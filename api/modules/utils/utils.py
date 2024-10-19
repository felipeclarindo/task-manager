from datetime import date, timedelta, datetime
from enum import StrEnum


class EstadoUser(StrEnum):
    LIBERADO = "liberado"
    BLOQUEADO = "bloqueado"


class TaskState(StrEnum):
    CONCLUIDO = "concluido"
    PENDENTE = "pendente"
    EM_PROGRESSO = "em progresso"


def check_user_state(validacoes: list) -> EstadoUser:
    for validacao in validacoes:
        if not validacao:
            return EstadoUser.BLOQUEADO
    return EstadoUser.LIBERADO


def date_today() -> str:

    data = date.today()
    return data.strftime("%Y/%m/%d")


def due_date(dias: int, createdAt: datetime = None, update: bool = False) -> str:
    dias = int(dias)
    delta = timedelta(days=dias)

    if not update:
        data = datetime.now() + delta
    else:
        if createdAt is None:
            raise ValueError("createdAt não pode ser None quando update é True.")
        data = createdAt + delta

    return data.strftime("%Y/%m/%d")


def get_data_criacao(cursor, id: int) -> datetime:
    command = "SELECT data_criacao FROM tarefas WHERE id = :id"
    cursor.execute(command, {"id": id})
    data_vencimento = cursor.fetchone()

    if data_vencimento is not None:
        data_vencimento = data_vencimento[0]
        return data_vencimento
    raise ValueError(f"Nenhuma data de criação encontrada para o ID: {id}")


def convert_data(data: str) -> str:
    print("convert_data")
    data = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
    return data.strftime("%d/%m/%Y")