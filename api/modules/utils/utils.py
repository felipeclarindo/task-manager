from datetime import date, timedelta, datetime
from enum import StrEnum


class EstadoUser(StrEnum):
    LIBERADO = "liberado"
    BLOQUEADO = "bloqueado"

class TaskState(StrEnum):
    CONCLUIDO = "concluido"
    PENDENTE = "pendente"
    EM_PROGRESSO = "em progresso"


def check_user_state(validacoes:list) -> EstadoUser:
    for validacao in validacoes:
        if not validacao:
            return EstadoUser.BLOQUEADO
    return EstadoUser.LIBERADO

def date_today() -> str:

    data = date.today()
    return data.strftime("%Y/%m/%d")

def due_date(dias: int, createdAt: str = None, update: bool = False) -> str:
    dias = int(dias)
    delta = timedelta(days=dias)
    if not update:
        data = date.today() + delta
    else:
        data = datetime.strptime(createdAt, "%d/%m/%Y") + delta
    return data.strftime("%Y/%m/%d")