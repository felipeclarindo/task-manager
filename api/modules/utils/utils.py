from datetime import date, timedelta, datetime
from enum import StrEnum


class EstadoUser(StrEnum):
    LIBERADO = "liberado"
    BLOQUEADO = "bloqueado"


def check_user_state(validacoes):
    for validacao in validacoes:
        if not validacao:
            return EstadoUser.BLOQUEADO
    else:
        return EstadoUser.LIBERADO


def date_today() -> str:
    data = date.today()
    return data.strftime("%Y/%m/%d")


def due_date(dias: int, update: False, createdAt: str = None) -> str:
    delta = timedelta(days=dias)
    if not update:
        data = date.today()
        data = data + delta

        return data.strftime("%Y/%m/%d")
    else:
        data = datetime.strptime(createdAt, "%d/%m/%Y") + delta
        return data.strftime("%Y/%m/%d") 
