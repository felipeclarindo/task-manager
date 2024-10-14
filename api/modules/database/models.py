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
    get_data_criacao,
    convert_data,
)
import json


class Crud:
    def __init__(self) -> None:
        self.connection = connect()

    # Validação de dados antes do envio
    def post_validate(self, titulo: str, prioridade: str, prazo: int) -> None:
        validacoes = [
            validate_title(titulo),
            validate_prioridade(prioridade),
            validate_prazo(prazo),
        ]
        self.user_state = check_user_state(validacoes)

    # Inserir dados no banco de dados
    def post(self, titulo: str, prioridade: str, prazo: int) -> dict:
        try:
            self.post_validate(titulo, prioridade, prazo)
            if self.user_state == EstadoUser.LIBERADO:
                data_criacao = date_today()
                data_vencimento = due_date(prazo, data_criacao)
                command = """
                    INSERT INTO tarefas (titulo, prioridade, status, data_vencimento, data_criacao)
                    VALUES (:titulo, :prioridade, :status, TO_DATE(:data_vencimento, 'YYYY-MM-DD'), TO_DATE(:data_criacao, 'YYYY-MM-DD'))
                """
                with self.connection.cursor() as cursor:
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
                return {
                    "status": "Success",
                    "message": "Tarefa adicionada com sucesso.",
                }
            else:
                raise Exception("Falha na validação.")
        except ValueError as e:
            return {"status": "valueError", "message": str(e)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Atualizar dados
    def put(self, id: int, titulo: str, prioridade: str, prazo: int) -> dict:
        try:
            self.post_validate(titulo, prioridade, prazo)

            if self.user_state == EstadoUser.LIBERADO:
                with self.connection.cursor() as cursor:
                    data_criacao = get_data_criacao(cursor, id)
                    data_vencimento = due_date(prazo, data_criacao, True)
                    print(data_vencimento)
                    command = """
                        UPDATE tarefas
                        SET titulo = :titulo,
                            data_vencimento = TO_DATE(:data_vencimento, 'YYYY-MM-DD'),
                            prioridade = :prioridade,
                            status = :status
                        WHERE id = :id
                    """
                    cursor.execute(
                        command,
                        {
                            "titulo": titulo,
                            "data_vencimento": data_vencimento,
                            "prioridade": prioridade,
                            "status": TaskState.PENDENTE,
                            "id": id,
                        },
                    )
                self.connection.commit()
                return {
                    "status": "Success",
                    "message": "Tarefa atualizada com sucesso.",
                }
            else:
                return {"status": "Error", "message": "Dados inválidos."}
        except ValueError as e:
            return {"status": "ValueError", "message": str(e)}
        except Exception as e:
            return {"status": "Error", "message": str(e)}

    # Atualizar um unico dado
    def patch(self, id: int, dado: str, novo_dado: str) -> dict:
        try:
            dado = dado.lower().strip()
            if dado not in ["titulo", "prazo", "prioridade", "status"]:
                raise ValueError("Nome de coluna inválido.")

            print(novo_dado)
            if dado == "prazo":
                cursor = self.connection.cursor()
                data_criacao = get_data_criacao(cursor, id)
                cursor.close()  
                novo_dado = due_date(int(novo_dado), data_criacao, True)

                command = f"UPDATE tarefas SET data_vencimento = TO_DATE(:novo_dado, 'YYYY-MM-DD') WHERE ID = :id"
            else:
                command = f"UPDATE tarefas SET {dado} = :novo_dado WHERE ID = :id"

            with self.connection.cursor() as cursor:
                cursor.execute(
                    command,
                    {
                        "novo_dado": novo_dado,
                        "id": id,
                    },
                )
            self.connection.commit()
            return {"status": "Success", "message": "Tarefa atualizada com sucesso."}
        except ValueError as e:
            return {"status": "ValueError", "message": str(e)}
        except Exception as e:
            return {"status": "Error", "message": str(e)}

    # Deletar
    def delete(self, id: int) -> dict:
        try:
            command = "DELETE FROM tarefas WHERE ID = :id"
            with self.connection.cursor() as cursor:
                cursor.execute(command, {"id": id})
            self.connection.commit()
            return {"status": "Success", "message": "Tarefa deletada com sucesso."}
        except ValueError as e:
            return {"status": "ValueError", "message": str(e)}
        except Exception as e:
            return {"status": "Error", "message": str(e)}

    # Obter todos os dados
    import json

    def get_all(self):
        try:
            command = "SELECT * FROM tarefas ORDER BY ID"
            with self.connection.cursor() as cursor:
                cursor.execute(command)
                tarefas = cursor.fetchall()
                columns = [column[0] for column in cursor.description]

                if tarefas:
                    tarefas_modificadas = []
                    for tarefa in tarefas:
                        tarefa_dict = {}
                        for i, dado in enumerate(tarefa):
                            if i in [4, 5]:
                                tarefa_dict[columns[i]] = convert_data(str(dado))
                            else:
                                tarefa_dict[columns[i]] = dado
                        tarefas_modificadas.append(tarefa_dict)

                    return {
                        "status": "Success",
                        "message": "Tarefas encontradas com sucesso.",
                        "response": json.dumps(tarefas_modificadas),
                    }

                return {"status": "Success", "message": "Nenhuma tarefa encontrada."}
        except ValueError as e:
            return {"status": "ValueError", "message": str(e)}
        except Exception as e:
            return {"status": "Error", "message": str(e)}

    # Obter dados por ID
    def get_with_id(self, id: int):
        try:
            command = "SELECT * FROM tarefas WHERE ID = :id"
            with self.connection.cursor() as cursor:
                cursor.execute(command, {"id": id})
                tarefa = cursor.fetchone()
                columns = [column[0] for column in cursor.description]

                if tarefa:
                    tarefa_dict = {}
                    for i, dado in enumerate(tarefa):
                        if i in [4, 5]:
                            tarefa_dict[columns[i]] = convert_data(str(dado))
                        else:
                            tarefa_dict[columns[i]] = dado

                    return {
                        "status": "Success",
                        "message": "Tarefa encontrada com sucesso",
                        "response": json.dumps(tarefa_dict),
                    }
                raise Exception(f"Tarefa com id {id} não encontrada.")
        except ValueError as e:
            return {"status": "ValueError", "message": str(e)}
        except Exception as e:
            return {"status": "Error", "message": str(e)}

    # Finalizando a conexão quando a instância é excluída
    def __del__(self):
        self.connection.close()
