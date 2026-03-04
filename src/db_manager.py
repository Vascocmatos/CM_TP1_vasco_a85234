# db_manager.py
import duckdb
import os

PARQUET_FILE = "tasks.parquet"

def save_to_db(data):
    """Guarda a lista de dicionários no DuckDB e exporta para Parquet."""
    con = duckdb.connect()

    con.execute("CREATE TABLE tasks (name VARCHAR, completed BOOLEAN)")
    

    for item in data:
        con.execute("INSERT INTO tasks VALUES (?, ?)", (item['name'], item['completed']))
    

    con.execute(f"COPY tasks TO '{PARQUET_FILE}' (FORMAT PARQUET)")
    con.close()

def load_from_db():
    """Carrega os dados do ficheiro Parquet, se existir."""
    if not os.path.exists(PARQUET_FILE):
        return []
    
    con = duckdb.connect()
    try:

        result = con.execute(f"SELECT name, completed FROM read_parquet('{PARQUET_FILE}')").fetchall()
        con.close()

        return [{"name": row[0], "completed": row[1]} for row in result]
    except Exception as e:
        print(f"Erro ao ler Parquet DB: {e}")
        con.close()
        return []