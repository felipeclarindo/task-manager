class ValidateError(Exception):
    pass


def validate_title(title: str) -> bool:
    try:
        if title:
            title = title.strip().lower()
            if title.isalnum():
                return True
            else:
                raise ValidateError(
                    "Titulo invalido, não é aceito caracteres especiais"
                )
        else:
            raise ValueError("O titulo não pode ser vazio.")
    except ValidateError as e:
        print(f"Erro de Validação: {e}")
    except ValueError as e:
        print(f"Erro de Valor: {e}")
    except Exception as e:
        print(f"Erro {e}")
    return False


def validate_prioridade(prioridade: str) -> bool:
    try:
        if prioridade:
            prioridade = prioridade.strip().lower()
            if prioridade in ["baixa", "media", "alta"]:
                return True
            else:
                raise ValidateError("Prioridade invalida.")
        else:
            raise ValueError("Prioridade não pode ser vazia.")
    except ValidateError as e:
        print(f"Erro de Validação: {e}")
    except ValueError as e:
        print(f"Erro de Valor: {e}")
    except Exception as e:
        print(f"Erro: {e}")
    return False


def validate_status(status: str) -> bool:
    try:
        if status:
            status = status.strip().lower()
            if status in ["concluido", "pendente", "em progresso"]:
                return True
            else:
                raise ValidateError("Status invalido!")
    except ValidateError as e:
        print(f"Erro de Validação: {e}")
    except Exception as e:
        print(f"Erro: {e}")
    return False
