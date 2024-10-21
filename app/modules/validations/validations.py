class ValidateError(Exception):
    pass

def validate_title(title: str) -> bool:
    if not title:
        raise ValueError("O título não pode ser vazio!")
    
    title = title.strip()
    if len(title) < 3:
        raise ValidateError("O título deve ter pelo menos 3 caracteres.")
    
    if not all(c.isalnum() or c.isspace() for c in title):
        raise ValidateError("O título não pode conter caracteres especiais.")

    return True


def validate_desc(descricao: str) -> bool:
    if not descricao:
        raise ValueError("A descrição não pode estar vazia!")

def validate_prioridade(prioridade: str) -> None:
    valid_prioridades = ["baixa", "media", "alta"]
    if prioridade not in valid_prioridades:
        raise ValueError(f"A prioridade deve ser uma das seguintes: {', '.join(valid_prioridades)}")

def validate_prazo(prazo: int) -> None:
    if prazo <= 0:
        raise ValueError("O prazo deve ser superior a data atual.")
    if not prazo:
        raise ValueError("O prazo não pode estar vazio!")
    
import re

def validate_email(email: str) -> bool:
    characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-_")

    if not email:
        raise ValueError("O e-mail não pode ser vazio.")

    is_in_chars = lambda c: c in characters and len(c) == 1

    try:
        user, domain = email.split("@")
    except ValueError:
        raise ValueError("O e-mail deve conter um '@'.")

    if not user or not all(is_in_chars(c) for c in user):
        raise ValidateError("E-mail inválido! Verifique o formato do e-mail.")

    domain_parts = domain.split(".")
    if len(domain_parts) < 2 or not all(part and all(is_in_chars(c) for c in part) for part in domain_parts):
        raise ValidateError("Formato de e-mail inválido!")