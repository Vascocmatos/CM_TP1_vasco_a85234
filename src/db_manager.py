# db_manager.py
import duckdb
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# 1. Carregar variáveis de ambiente
load_dotenv()
CHAVE = os.getenv("SECRET_KEY")
cipher = Fernet(CHAVE.encode()) if CHAVE else None

PARQUET_FILE = "tasks.parquet"
ENCRYPTED_FILE = "tasks.crypt"

def save_to_db(data):
    """Guarda dados, exporta para Parquet e depois ENCRIPTA o ficheiro."""
    # O teu código original do DuckDB
    con = duckdb.connect()
    con.execute("CREATE OR REPLACE TABLE tasks (name VARCHAR, completed BOOLEAN)")
    for item in data:
        con.execute("INSERT INTO tasks VALUES (?, ?)", (item['name'], item['completed']))
    
    con.execute(f"COPY tasks TO '{PARQUET_FILE}' (FORMAT PARQUET)")
    con.close()

    # --- Lógica de Encriptação ---
    with open(PARQUET_FILE, "rb") as f:
        conteudo_original = f.read()
    
    conteudo_encriptado = cipher.encrypt(conteudo_original)
    
    with open(ENCRYPTED_FILE, "wb") as f:
        f.write(conteudo_encriptado)
    
    # IMPORTANTE: Remover o Parquet original para segurança
    if os.path.exists(PARQUET_FILE):
        os.remove(PARQUET_FILE)

def load_from_db():
    """Lê o ficheiro encriptado, desencripta-o temporariamente e carrega no DuckDB."""
    if not os.path.exists(ENCRYPTED_FILE):
        return []
    
    try:
        # --- Lógica de Desencriptação ---
        with open(ENCRYPTED_FILE, "rb") as f:
            conteudo_encriptado = f.read()
        
        conteudo_desencriptado = cipher.decrypt(conteudo_encriptado)
        
        # Guardamos num ficheiro temporário para o DuckDB conseguir ler
        with open(PARQUET_FILE, "wb") as f:
            f.write(conteudo_desencriptado)

        con = duckdb.connect()
        result = con.execute(f"SELECT name, completed FROM read_parquet('{PARQUET_FILE}')").fetchall()
        con.close()

        # Limpar o ficheiro temporário após a leitura
        os.remove(PARQUET_FILE)

        return [{"name": row[0], "completed": row[1]} for row in result]
        
    except Exception as e:
        print(f"Erro na segurança/leitura: {e}")
        return []