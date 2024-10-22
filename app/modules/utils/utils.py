import streamlit as st 
import requests
import json
from datetime import datetime 

#Função para pular linhas dependendo do numero passado
def pula_linha(n:int):
    for i in range(0,n):
        st.write(" ")

#Função que retorna uma lista com dicionário de tarefas vinda do getAll
def visualizar() -> list[dict]:
    url = " http://127.0.0.1:8000/api/tasks/"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    if len(data) == 2:
        return []
    return data['response']
    
#Função que retorna uma lista com dicionário de tarefas vinda do getById
def vizualizar_tarefa(id:int) -> dict:
    url = f" http://127.0.0.1:8000/api/tasks/{id}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    if len(data) == 2:
        return []
    return data['response']

#Função que realiza o delete de uma tarefa
def apagar(id:int):
    url = f" http://127.0.0.1:8000/api/tasks/{id}"
    response = requests.delete(url)
    response.raise_for_status()
    
#Função que realiza o post de uma tarefa
def criar_tarefa(data:json) -> dict:
    url = " http://127.0.0.1:8000/api/tasks/"
    response = requests.post(url,data)
    response.raise_for_status()
    return response.json()

def atualizar(id:int, data:json):
    url = f"http://127.0.0.1:8000/api/tasks/{id}"
    response = requests.put(url, data)
    response.raise_for_status()
    return response.json()


def lista_cronograma(lista_tarefas: list[dict]) -> list[dict]:
    lista_ordenada = []
    for tarefa in lista_tarefas:
        new_dict = {}
        point_counter = 0
        if tarefa['STATUS'] == 'alta':
            point_counter += 2
        elif tarefa['STATUS'] == 'media':
            point_counter += 1
        if tarefa['PRIORIDADE'] == 'em progresso':
            point_counter += 2
        elif tarefa['PRIORIDADE'] == 'pendente':
            point_counter += 1
        if (datetime.strptime(tarefa["DATA_VENCIMENTO"], "%d/%m/%Y").date() - datetime.strptime(tarefa["DATA_CRIACAO"], "%d/%m/%Y").date()).days < 4:
            point_counter += 2
        elif (datetime.strptime(tarefa["DATA_VENCIMENTO"], "%d/%m/%Y").date() - datetime.strptime(tarefa["DATA_CRIACAO"], "%d/%m/%Y").date()).days < 8:
            point_counter += 1
        new_dict['titulo'] = tarefa["TITULO"]
        new_dict['prioridade'] = tarefa["PRIORIDADE"]
        new_dict['status'] = tarefa["STATUS"]
        new_dict['dias para entrega'] = (datetime.strptime(tarefa["DATA_VENCIMENTO"], "%d/%m/%Y").date() - datetime.strptime(tarefa["DATA_CRIACAO"], "%d/%m/%Y").date()).days
        new_dict['pontos'] = point_counter
        
        lista_ordenada.append(new_dict)

    lista_ordenada.sort(key=lambda x: (x['pontos'], -x['dias para entrega']), reverse=True)
    return lista_ordenada
        
        