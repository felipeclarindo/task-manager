from config import connect
from .validations.validations import (
    validate_prioridade,
    validate_status,
    validate_title,
)
from .utils.utils import check_user_state, EstadoUser, date_today, due_date
from datetime import date, datetime
import json


class Crud:
    def __init__(self) -> None:
        self.connection = connect()

    # Validação de dados antes do envio
    def post_validate(self, title: str, prioridade: str, prazo: int) -> None:
        self.validacoes = [
            validate_title(title),
            validate_prioridade(prioridade),
            validate_prazo(prazo),
        ]
        self.user_state = check_user_state(self.validacoes)

    # Inserir dados no banco de dados
    def post(
        self,
        titulo: str,
        prioridade: str,
        prazo: int,
    ) -> dict:
        try:
            self.post_validate(titulo, prioridade, status, prazo)
            if self.user_state == EstadoUser.LIBERADO:
                data_criacao = date_today()
                data_vencimento = due_date(data_criacao, prazo)
                command = f"INSERT INTO relatos (titulo, prioridade, status, data_vencimento, data_criacao) VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), TO_DATE(:5, 'YYYY-MM-DD'))"                cursor = self.connection.cursor()
                cursor.execute(
                    command,
                    (
                        titulo,
                        prioridade,
                        generate_state(data_criacao, data_vencimento),
                        data_vencimento,
                        data_criacao
                    ),
                )
                self.connection.commit()
                cursor.close()
                return {"status": "success"}
            else:
                return {"status": "error", "message": "404"}
        except ValueError as v:
            return {"status": "error", "message": str(v)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Atualizar dados
    def put(
        self,
        id: int,
        titulo: str,
        prioridade: str,
        prazo: int
    ) -> dict:
        try:
            self.post_validate(titulo, prioridade, status)
            if self.user_state == EstadoUser.LIBERADO:
                command = "UPDATE relatos SET titulo = :titulo, data_vencimento = :TO_DATE(data_vencimento, 'YYYY-MM-DD'), prioridade = :prioridade, status = :status WHERE id = :id"
                cursor = self.connection.cursor()
                cursor.execute(
                    command,
                    {
                        "titulo": titulo,
                        "data_vencimento": due_date(data_vencimento),
                        "prioridade": prioridade,
                        "status": status,
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
                command = f"UPDATE relatos SET {dado} = :TO_DATE(novo_dado, 'YYYY-MM-DD') WHERE ID = :id"
                cursor = self.connection.cursor()
                cursor.execute(command, {"novo_dado": due_date(novo_dado), "id": id})
                cursor.close()
                self.connection.commit()
                return {"status": "success"}
            else:
                command = f"UPDATE relatos SET {dado} = :novo_dado WHERE ID = :id"
                cursor = self.connection.cursor()
                cursor.execute(command, {"novo_dado": novo_dado, "id": id})
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
            command = f"SELECT * FROM relatos WHERE ID = :id"
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