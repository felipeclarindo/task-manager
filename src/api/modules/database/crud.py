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
from fastapi import HTTPException
from typing import Optional


class Crud:
    def __init__(self) -> None:
        self.connection = connect()
        self.notification = Notificador()

        # Conectar e criar a tabela se não existir
        if self.connection:
            create_table_if_not_exists(self.connection)

    # Validação de dados
    def validate_fields(self, titulo: str, descricao: str, prioridade: str, prazo: int, email: str) -> None:
        validacoes = [
            validate_title(titulo),
            validate_desc(descricao),    
            validate_prioridade(prioridade),
            validate_prazo(prazo),
            validate_email(email),
        ]
        self.user_state = check_user_state(validacoes)

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
                            if i in [5, 6]:
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
            raise HTTPException(status_code=400, detail=str(e))
        
    # Obtendo dados por ID
    def get_by_id(self, id: int):
        try:
            command = "SELECT * FROM tarefas WHERE ID = :id"
            with self.connection.cursor() as cursor:
                cursor.execute(command, {"id": id})
                tarefa = cursor.fetchone()
                columns = [column[0] for column in cursor.description]

                if tarefa:
                    tarefa_dict = {}
                    for i, dado in enumerate(tarefa):
                        if i in [5, 6]:
                            tarefa_dict[columns[i]] = convert_data(str(dado))
                        else:
                            tarefa_dict[columns[i]] = dado

                    return {
                        "status": "Success",
                        "message": "Tarefa encontrada com sucesso",
                        "response": tarefa_dict
                    }
                raise HTTPException(status_code=404, detail=f"Tarefa com id {id} não encontrada.")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    # Inserir dados
    def post(self, titulo: str, descricao: str, prioridade: str, prazo: int, email: str) -> dict:
        try:
            self.validate_fields(titulo, descricao, prioridade, prazo, email)

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
                subject = f"Tarefa Criada: {titulo}"
                message_body = (
                    f"Uma nova tarefa foi adicionada:\n\n"
                    f"Título: {titulo};\n"
                    f"Descrição: {descricao};\n"
                    f"Prioridade: {prioridade};\n"
                    f"Prazo de: {prazo} dia(s);\n"
                )
                print("Enviando o email")
                self.notification.send_email(email, subject, message_body)

                return {
                    "status": "Success",
                    "message": "Tarefa criada com sucesso.",
                }
            else:
                raise HTTPException(status_code=400, detail="Falha na validação.")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    # Atualizar dados
    def put(self, id: int, titulo: str, descricao: str, prioridade: str, prazo: int, email: str, status: Optional[str] = None) -> dict:
        try:
            self.validate_fields(titulo, descricao, prioridade, prazo, email)

            if self.user_state == EstadoUser.LIBERADO:
                with self.connection.cursor() as cursor:
                    data_criacao = get_data_criacao(cursor, id)
                    data_vencimento = due_date(prazo, data_criacao, True)

                    # Verificar e validar o status recebido
                    if status is None:
                        status = TaskState.PENDENTE
                    elif status not in TaskState.__members__.values():
                        raise HTTPException(status_code=400, detail="Status inválido.")

                    command = """
                        UPDATE tarefas
                        SET titulo = :titulo,
                            descricao = :descricao,
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
                            "status": status,  
                            "id": id,
                            "email": email
                        },
                    )
                self.connection.commit()

                # Enviar notificação por e-mail
                subject = f"Tarefa Atualizada: {titulo}"
                message_body = (
                    f"Uma tarefa foi atualizada:\n\n"
                    f"Título: {titulo};\n"
                    f"Descrição: {descricao};\n"
                    f"Prioridade: {prioridade};\n"
                    f"Prazo de: {prazo} dia(s);\n"
                    f"Status: {status};\n"
                )
                self.notification.send_email(email, subject, message_body)

                return {
                    "status": "Success",
                    "message": "Tarefa atualizada com sucesso.",
                }
            else:
                raise HTTPException(status_code=400, detail="Dados inválidos.")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    # Deletar
    def delete(self, id: int) -> dict:
        try:
            select_email = "SELECT email FROM tarefas WHERE ID = :id"
            delete_command = "DELETE FROM tarefas WHERE ID = :id"
            
            with self.connection.cursor() as cursor:
                cursor.execute(select_email, {"id": id})
                result = cursor.fetchone() 

                if not result:
                    raise HTTPException(status_code=404, detail=f"Tarefa com id {id} não encontrada.")

                email = result[0]

                cursor.execute(delete_command, {"id": id})
            
            self.connection.commit()

            subject = "Tarefa Deletada"
            message_body = f"A sua tarefa com id: {id} foi apagada com sucesso!\n"

            self.notification.send_email(email, subject, message_body)
            
            return {"status": "Success", "message": "Tarefa deletada com sucesso."}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
