# db_manager.py
import duckdb
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()
CHAVE = os.getenv("SECRET_KEY")
cipher = Fernet(CHAVE.encode()) if CHAVE else None

PARQUET_FILE = "tasks.parquet"
ENCRYPTED_FILE = "tasks.crypt"

def save_to_db(data):
    con = duckdb.connect()
    # Adicionado user_id à tabela
    con.execute("CREATE OR REPLACE TABLE tasks (user_id VARCHAR, name VARCHAR, completed BOOLEAN)")
    
    for item in data:
        # Garante que salva o user_id (se não existir, usa 'default')
        con.execute("INSERT INTO tasks VALUES (?, ?, ?)", (item.get('user_id', 'default'), item['name'], item['completed']))
    
    con.execute(f"COPY tasks TO '{PARQUET_FILE}' (FORMAT PARQUET)")
    con.close()

    with open(PARQUET_FILE, "rb") as f:
        conteudo_original = f.read()
    
    conteudo_encriptado = cipher.encrypt(conteudo_original)
    
    with open(ENCRYPTED_FILE, "wb") as f:
        f.write(conteudo_encriptado)
    
    if os.path.exists(PARQUET_FILE):
        os.remove(PARQUET_FILE)

def load_from_db():
    if not os.path.exists(ENCRYPTED_FILE):
        return []
    
    try:
        with open(ENCRYPTED_FILE, "rb") as f:
            conteudo_encriptado = f.read()
        
        conteudo_desencriptado = cipher.decrypt(conteudo_encriptado)
        
        with open(PARQUET_FILE, "wb") as f:
            f.write(conteudo_desencriptado)

        con = duckdb.connect()
        # Lê agora também o user_id
        result = con.execute(f"SELECT user_id, name, completed FROM read_parquet('{PARQUET_FILE}')").fetchall()
        con.close()

        os.remove(PARQUET_FILE)

        return [{"user_id": row[0], "name": row[1], "completed": row[2]} for row in result]
        
    except Exception as e:
        print(f"Erro na segurança/leitura: {e}")
        return []