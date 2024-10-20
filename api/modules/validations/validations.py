import re

class ValidateError(Exception):
    pass


def validate_title(title: str) -> bool:
    try:
        if title:
            title = title.strip().lower()
            if all(c.isalnum() or c.isspace() for c in title):
                return True
            else:
                raise ValidateError(
                    "Título inválido, não é aceito caracteres especiais"
                )
        else:
            raise ValueError("O título não pode ser vazio.")
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
            if prioridade in ["baixa", "media", "média", "alta"]:
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


def validate_prazo(prazo: int) -> bool:
    try:
        prazo = str(prazo)
        if prazo:
            prazo = prazo.strip()
            if prazo.isdigit():
                if int(prazo) > 0:
                    return True
                else:
                    raise ValueError("O Prazo mínimo é 1.")
            else:
                raise ValueError(f"O Prazo precisa ser um número.")
        else:
            raise ValueError("Prazo não pode ser vazio.")
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
        else:
            raise ValueError("Status não pode ser vazio.")
    except ValidateError as e:
        print(f"Erro de Validação: {e}")
    except ValueError as e:
        print(f"Erro de Valor: {e}")
    except Exception as e:
        print(f"Erro: {e}")
    return False


def validate_email(email: str) -> bool:
    try:
        if not email:
            raise ValueError("O número não pode ser vázio.")
        
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

        if re.match(email_regex, email):
            return True
        else:
            raise ValueError("Formato de e-mail inválido.")
            
    except ValidateError as e:
        print(f"Erro de Validação: {e}")
    except ValueError as e:
        print(f"Erro de Valor: {e}")
    except Exception as e:
        print(f"Erro: {e}")

    return False

def validate_desc(descricao: str) -> bool:
    try:
        if not descricao:
            raise ValueError("A descrição não pode ser vázia")
        
        return True
        
    except ValidateError as e:
        print(f"Erro de Validação: {e}")
    except ValueError as e:
        print(f"Erro de Valor: {e}")
    except Exception as e:
        print(f"Erro: {e}")

    return False