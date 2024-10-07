from .config import connect
from ..validations.validations import (
    validate_prioridade,
    validate_prazo,
    validate_title,
)
from ..utils.utils import (
    check_user_state,
    EstadoUser,
    TaskState,
    date_today,
    due_date,
)
from datetime import date, datetime
import json


class Crud:
    def __init__(self) -> None:
        self.connection = connect()
        command = """CREATE TABLE IF NOT EXISTS tarefas (
                id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                titulo VARCHAR(255) NOT NULL,
                prioridade VARCHAR(50) NOT NULL,
                status VARCHAR(50) NOT NULL,
                data_vencimento DATE NOT NULL,
                data_criacao DATE NOT NULL
                )
                """
        cursor = self.connection.cursor()
        cursor.execute(command)
        cursor.close()

    # Validação de dados antes do envio
    def post_validate(self, titulo: str, prioridade: str, prazo: str) -> None:
        validacoes = [
            validate_title(titulo),
            validate_prioridade(prioridade),
            validate_prazo(prazo),
        ]
        print(validacoes)
        self.user_state = check_user_state(validacoes)

    # Inserir dados no banco de dados
    def post(
        self,
        titulo: str,
        prioridade: str,
        prazo: str,
    ) -> dict:
        try:
            self.post_validate(titulo, prioridade, prazo)
            if self.user_state == EstadoUser.LIBERADO:
                data_criacao = date_today()
                data_vencimento = due_date(prazo, data_criacao)
                command = f"INSERT INTO tarefas (titulo, prioridade, status, data_vencimento, data_criacao) VALUES (:titulo, :prioridade, :status, TO_DATE(:data_vencimento, 'YYYY-MM-DD'), TO_DATE(:data_criacao, 'YYYY-MM-DD'))"
                cursor = self.connection.cursor()
                cursor.execute(
                    command,
                    {
                        "titulo": titulo,
                        "prioridade": prioridade,
                        "status": TaskState.PENDENTE,
                        "data_vencimento": data_vencimento,
                        "data_criacao": data_criacao,
                    },
                )
                self.connection.commit()
                cursor.close()
                return {"status": "success"}
            else:
                raise Exception("Falha na validação.")
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Atualizar dados
    def put(self, id: int, titulo: str, prioridade: str, prazo: str) -> dict:
        try:
            self.post_validate(titulo, prioridade, prazo)
            if self.user_state == EstadoUser.LIBERADO:

                command = "UPDATE tarefas SET titulo = :titulo, data_vencimento = TO_DATE(:data_vencimento, 'YYYY-MM-DD'), prioridade = :prioridade, status = :status WHERE id = :id"
                cursor = self.connection.cursor()
                cursor.execute(
                    command,
                    {
                        "titulo": titulo,
                        "data_vencimento": due_date(prazo, ""),
                        "prioridade": prioridade,
                        "status": TaskState.PENDENTE,
                        "id": id,
                    },
                )
                cursor.close()
                self.connection.commit()
                return {"status": "success"}
            else:
                return {"status": "error", "message": "Dados inválidos."}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Atualizar selecionando campo
    def patch(self, id: int, dado: str | int, novo_dado: str | int) -> dict:
        try:
            if dado not in ["titulo", "data_vencimento", "prioridade", "status"]:
                raise ValueError("Nome de coluna inválido.")
            if dado == "data_vencimento":
                command = f"UPDATE tarefas SET :dado = TO_DATE(:novo_dado, 'YYYY-MM-DD') WHERE ID = :id"
                cursor = self.connection.cursor()
                cursor.execute(
                    command, {"dado": dado, "novo_dado": due_date(novo_dado), "id": id}
                )
                cursor.close()
                self.connection.commit()
                return {"status": "success"}
            else:
                command = f"UPDATE tarefas SET :dado = :novo_dado WHERE ID = :id"
                cursor = self.connection.cursor()
                cursor.execute(
                    command,
                    {
                        "dado": dado,
                        "novo_dado": novo_dado,
                        "id": id,
                    },
                )
                cursor.close()
                self.connection.commit()
                return {"status": "success"}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Deletar
    def delete(self, id: int) -> dict:
        try:
            command = f"DELETE FROM tarefas WHERE ID = :id"
            cursor = self.connection.cursor()
            cursor.execute(command, {"id": id})
            self.connection.commit()
            cursor.close()
            return {"status": "success"}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Obter todos os dados
    def get(self):
        try:
            command = "SELECT * FROM tarefas"
            cursor = self.connection.cursor()
            cursor.execute(command)
            tarefas = cursor.fetchall()
            cursor.close()
            return {
                "status": "success",
                "message": json.dumps([dict(tarefa) for tarefa in tarefas]),
            }
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Obter dados por ID
    def get_with_id(self, id: int):
        try:
            command = f"SELECT * FROM tarefas WHERE ID = :id"
            cursor = self.connection.cursor()
            cursor.execute(command, {"id": id})
            tarefa = cursor.fetchone()
            cursor.close()
            return {"status": "success", "message": json.dumps([dict(tarefa)])}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Finalizando a conexão quando instancia excluida
    def __del__(self):
        self.connection.close()
