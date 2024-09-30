from dotenv import load_dotenv
from time import sleep
import oracledb
import os

load_dotenv()


def connect():
    try:
        username = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        service_name = os.getenv("DB_SERVICE_NAME")

        dsn = f"{username}/{password}@{host}:{port}/{service_name}"
        print(f"Conectando ao banco de dados em {host}:{port} como {username}...")
        sleep(1)
        connection = oracledb.connect(dsn)
        print("Conexão feita com sucesso!")
        return connection
    except Exception:
        print("Falha na conexão.")
    return None
