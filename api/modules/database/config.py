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

        dsn = f"{host}:{port}/{service_name}"
        print(f"Conectando ao banco de dados em {host}:{port} como {username}...")
        sleep(1)

        # Conectando ao banco de dados
        connection = oracledb.connect(user=username, password=password, dsn=dsn)
        print("Conexão feita com sucesso!")
        return connection
    except oracledb.DatabaseError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def create_table_if_not_exists(connection):
    try:
        cursor = connection.cursor()

        # Verificar se a tabela já existe (garantindo maiúsculas no nome da tabela)
        cursor.execute("""
            SELECT table_name FROM user_tables WHERE table_name = 'TAREFAS'
        """)
        result = cursor.fetchone()

        if result:
            print("Tabela já existe no banco.")
        else:
            # Criar a tabela se ela não existir
            sql = """
                CREATE TABLE TAREFAS (
                    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    titulo VARCHAR2(100) NOT NULL,
                    descricao VARCHAR2(250),
                    prioridade VARCHAR2(50) NOT NULL,
                    status VARCHAR2(50) NOT NULL,
                    data_vencimento DATE NOT NULL,
                    data_criacao DATE NOT NULL,
                    email VARCHAR2(80) NOT NULL
                )
            """
            cursor.execute(sql)
            connection.commit()
            print("Tabela criada com sucesso no banco!")
    except oracledb.DatabaseError as e:
        print(f"Erro ao criar a tabela: {e}")
    finally:
        cursor.close()

# Conectar e criar a tabela
connection = connect()
if connection:
    create_table_if_not_exists(connection)
    connection.close()
