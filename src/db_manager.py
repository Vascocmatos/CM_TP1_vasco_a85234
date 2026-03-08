# db_manager.py
import duckdb
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Carregamento de configurações sensíveis (SECRET_KEY)
load_dotenv()
CHAVE = os.getenv("SECRET_KEY")

# Inicialização do motor de encriptação Fernet
cipher = Fernet(CHAVE.encode()) if CHAVE else None

# Definição dos ficheiros de persistência
PARQUET_FILE = "tasks.parquet"
ENCRYPTED_FILE = "tasks.crypt"

def save_to_db(data):
    """Guarda as tarefas num ficheiro Parquet e encripta-o para segurança."""
    con = duckdb.connect()
    
    # Criação da tabela com suporte a multi-utilizador (user_id)
    con.execute("CREATE OR REPLACE TABLE tasks (user_id VARCHAR, name VARCHAR, completed BOOLEAN)")
    
    # Inserção de dados em lote
    for item in data:
        con.execute("INSERT INTO tasks VALUES (?, ?, ?)", 
                    (item.get('user_id', 'default'), item['name'], item['completed']))
    
    # Exportação para formato Parquet (eficiente para armazenamento)
    con.execute(f"COPY tasks TO '{PARQUET_FILE}' (FORMAT PARQUET)")
    con.close()

    # Leitura do ficheiro Parquet para encriptação
    with open(PARQUET_FILE, "rb") as f:
        conteudo_original = f.read()
    
    # Encriptação simétrica dos dados
    conteudo_encriptado = cipher.encrypt(conteudo_original)
    
    # Escrita do ficheiro final encriptado e limpeza do ficheiro temporário
    with open(ENCRYPTED_FILE, "wb") as f:
        f.write(conteudo_encriptado)
    
    if os.path.exists(PARQUET_FILE):
        os.remove(PARQUET_FILE)

def load_from_db():
    """Desencripta e carrega as tarefas da base de dados DuckDB."""
    if not os.path.exists(ENCRYPTED_FILE):
        return []
    
    try:
        # Leitura e desencriptação dos dados
        with open(ENCRYPTED_FILE, "rb") as f:
            conteudo_encriptado = f.read()
        
        conteudo_desencriptado = cipher.decrypt(conteudo_encriptado)
        
        # Escrita temporária do ficheiro Parquet para leitura pelo DuckDB
        with open(PARQUET_FILE, "wb") as f:
            f.write(conteudo_desencriptado)

        con = duckdb.connect()
        # Consulta SQL para recuperar as tarefas
        result = con.execute(f"SELECT user_id, name, completed FROM read_parquet('{PARQUET_FILE}')").fetchall()
        con.close()

        # Limpeza do ficheiro temporário após leitura
        os.remove(PARQUET_FILE)

        # Mapeamento dos resultados para formato de dicionário Python
        return [{"user_id": row[0], "name": row[1], "completed": row[2]} for row in result]
        
    except Exception as e:
        print(f"Erro na segurança/leitura da base de dados: {e}")
        return []