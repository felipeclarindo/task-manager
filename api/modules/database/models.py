from .config import connect, create_table_if_not_exists
from ..notification.notification import Notificador
from ..validations.validations import (
    validate_prioridade,
    validate_prazo,
    validate_title,
    validate_email,
    validate_desc
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

class Crud:
    def __init__(self) -> None:
        self.connection = connect()
        self.notification = Notificador()

        # Conectar e criar a tabela se não existir
        if self.connection:
            create_table_if_not_exists(self.connection)

    # Pegando todos os dados
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
                        "response": tarefas_modificadas,
                    }

                return {"status": "Success", "message": "Nenhuma tarefa encontrada."}
        except ValueError as e:
            return {"status": "ValueError", "message": str(e)}
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        
    # Obtendo dados por ID
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
                        "response": tarefa_dict
                    }
                raise Exception(f"Tarefa com id {id} não encontrada.")
        except ValueError as e:
            return {"status": "ValueError", "message": str(e)}
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        
    # Validação de dados antes do envio
    def post_validate(self, titulo: str, descricao: str, prioridade: str, prazo: int, email: str) -> None:
        validacoes = [
            validate_title(titulo),
            validate_desc(descricao),    
            validate_prioridade(prioridade),
            validate_prazo(prazo),
            validate_email(email),
        ]
        self.user_state = check_user_state(validacoes)

    # Inserir dados
    def post(self, titulo: str, descricao: str, prioridade: str, prazo: int, email: str) -> dict:
        try:
            self.post_validate(titulo, descricao, prioridade, prazo, email)

            if self.user_state == EstadoUser.LIBERADO:
                data_criacao = date_today()
                data_vencimento = due_date(prazo, data_criacao)

                command = """
                    INSERT INTO tarefas (titulo, descricao, prioridade, status, data_vencimento, data_criacao, email)
                    VALUES (:titulo, :descricao, :prioridade, :status, TO_DATE(:data_vencimento, 'YYYY-MM-DD'), TO_DATE(:data_criacao, 'YYYY-MM-DD'), :email)
                """
                with self.connection.cursor() as cursor:
                    cursor.execute(
                        command,
                        {
                            "titulo": titulo,
                            "descricao": descricao,
                            "prioridade": prioridade,
                            "status": TaskState.PENDENTE,
                            "data_vencimento": data_vencimento,
                            "data_criacao": data_criacao,
                            "email": email
                        },
                    )
                self.connection.commit()

                # Enviar notificação por e-mail
                subject = f"Tarefa Adicionada: {titulo}"
                message_body = (
                    f"Uma nova tarefa foi adicionada:\n"
                    f"Título: {titulo}\n"
                    f"Descrição: {descricao}\n"
                    f"Prioridade: {prioridade}\n"
                    f"Data de Vencimento: {data_vencimento}\n"
                    f"Data de Criação: {data_criacao}\n"
                )
                self.notification.send_email(email, subject, message_body)

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
    def put(self, id: int, titulo: str, descricao: str, prioridade: str, prazo: int, email: str) -> dict:
        try:
            self.post_validate(titulo, descricao, prioridade, prazo, email)

            if self.user_state == EstadoUser.LIBERADO:
                with self.connection.cursor() as cursor:
                    data_criacao = get_data_criacao(cursor, id)
                    data_vencimento = due_date(prazo, data_criacao, True)

                    command = """
                        UPDATE tarefas
                        SET titulo = :titulo,
                            descricao = :descricao
                            data_vencimento = TO_DATE(:data_vencimento, 'YYYY-MM-DD'),
                            prioridade = :prioridade,
                            status = :status,
                            email = :email
                        WHERE id = :id
                    """
                    cursor.execute(
                        command,
                        {
                            "titulo": titulo,
                            "descricao": descricao,
                            "data_vencimento": data_vencimento,
                            "prioridade": prioridade,
                            "status": TaskState.PENDENTE,
                            "id": id,
                            "email": email
                        },
                    )
                self.connection.commit()

                # Enviar notificação por e-mail
                subject = f"Tarefa Adicionada: {titulo}"
                message_body = (
                    f"Uma nova tarefa foi atualizada:\n"
                    f"Título: {titulo}\n"
                    f"Descrição: {descricao}\n"
                    f"Prioridade: {prioridade}\n"
                    f"Data de Vencimento: {data_vencimento}\n"
                    f"Data de Criação: {data_criacao}\n"
                )
                self.notification.send_email(email, subject, message_body)

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
            if dado not in ["titulo", "descricao", "prazo", "prioridade", "status", "email"]:
                raise ValueError("Nome de coluna inválido.")

            # Obter os dados atuais da tarefa
            with self.connection.cursor() as cursor:
                command = "SELECT * FROM tarefas WHERE ID = :id"
                cursor.execute(command, {"id": id})
                tarefa_atual = cursor.fetchone()
                
                if not tarefa_atual:
                    raise Exception(f"Tarefa com id {id} não encontrada.")
                columns = [column[0] for column in cursor.description]
                tarefa_dict = {columns[i]: tarefa_atual[i] for i in range(len(columns))}

            if dado == "prazo":
                data_criacao = tarefa_dict["data_criacao"]  # Supondo que "data_criacao" seja a coluna correta
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

            # Enviar notificação por e-mail
            subject = f"Tarefa Atualizada: {tarefa_dict['titulo']}"
            message_body = (
                f"A tarefa foi atualizada:\n"
                f"Título: {tarefa_dict['titulo']}\n"
                f"Descrição: {tarefa_dict['descricao']}\n"
                f"Prioridade: {tarefa_dict['prioridade']}\n"
                f"Data de Vencimento: {tarefa_dict['data_vencimento']}\n"
                f"Data de Criação: {tarefa_dict['data_criacao']}\n"
            )
            self.notification.send_email(tarefa_dict['email'], subject, message_body)

            return {"status": "Success", "message": "Tarefa atualizada com sucesso."}
        except ValueError as e:
            return {"status": "ValueError", "message": str(e)}
        except Exception as e:
            return {"status": "Error", "message": str(e)}


    # Deletar
    def delete(self, id: int) -> dict:
        try:
            # Obter os dados da tarefa antes de deletar
            command = "SELECT * FROM tarefas WHERE ID = :id"
            with self.connection.cursor() as cursor:
                cursor.execute(command, {"id": id})
                tarefa = cursor.fetchone()
                if not tarefa:
                    raise Exception(f"Tarefa com id {id} não encontrada.")
                columns = [column[0] for column in cursor.description]
                tarefa_dict = {columns[i]: tarefa[i] for i in range(len(columns))}

            command = "DELETE FROM tarefas WHERE ID = :id"
            with self.connection.cursor() as cursor:
                cursor.execute(command, {"id": id})
            self.connection.commit()

            # Enviar notificação por e-mail
            subject = f"Tarefa Deletada: {tarefa_dict['titulo']}"
            message_body = (
                f"A tarefa foi deletada:\n"
                f"Título: {tarefa_dict['titulo']}\n"
                f"Descrição: {tarefa_dict['descricao']}\n"
                f"Prioridade: {tarefa_dict['prioridade']}\n"
                f"Data de Vencimento: {tarefa_dict['data_vencimento']}\n"
                f"Data de Criação: {tarefa_dict['data_criacao']}\n"
            )
            self.notification.send_email(tarefa_dict['email'], subject, message_body)

            return {"status": "Success", "message": "Tarefa deletada com sucesso."}
        except ValueError as e:
            return {"status": "ValueError", "message": str(e)}
        except Exception as e:
            return {"status": "Error", "message": str(e)}

