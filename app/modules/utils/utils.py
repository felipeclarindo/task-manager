import streamlit as st 
import requests
import json

#Função para pular linhas dependendo do numero passado
def pula_linha(n:int):
    for i in range(0,n):
        st.write(" ")

#Função que retorna uma lista com dicionario de tarefas vinda do getAll
def visualizar() -> list[dict]:
    url = " http://127.0.0.1:8000/api/tasks/"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    if len(data) == 2:
        return []
    return data['response']
    
#Função que retorna uma lista com dicionario de tarefas vinda do getById
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