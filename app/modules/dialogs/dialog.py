import streamlit as st 
from datetime import datetime 
import requests
import json
import time
from ..utils.utils import criar_tarefa, vizualizar_tarefa, apagar

#Funções dialog criam uma caixa de dialogo com o usuario

#Função para o botão nova tarefa, onde o usuario colocara as informações necessarias para criar uma nova tarefas
@st.dialog("Nova Tarefa")
def nova_tarefa():
    titulo = st.text_input("Titulo: ")
    descricao = st.text_input("Descrição: ")
    prioridade = st.selectbox("Prioridade", ["baixa", "media", "alta"]) 
    prazo = st.date_input("Prazo", datetime.today()) 
    diferença = prazo - datetime.today().date()
    prazo = diferença.days
    email = st.text_input("E-mail: ")
    if st.button("Criar"):
        tarefa = {"titulo": titulo, "descricao":descricao, "prioridade": prioridade, "prazo": prazo,"email": email}
        try:
            resposta_api = criar_tarefa(json.dumps(tarefa))
            st.success(resposta_api["message"])
            time.sleep(1)
            st.rerun()
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 422:
                st.error("Erro de validação: os dados enviados não estão corretos.")
            else:
                st.error(f"Erro ao criar a tarefa: {err}")
            
            st.write("Resposta da API:", err.response.text)

        except json.JSONDecodeError:
            st.error("Erro ao processar a resposta da API. Resposta inválida.")

        except Exception as e:
            st.error(f"Ocorreu um erro inesperado: {e}")
        
#Função para o botão info, onde o usuario poderá ver todas as informações daquela tarefa
@st.dialog("Infos Da Tarefa")
def infos_tarefa(id:int):
    tarefa = vizualizar_tarefa(id)
    st.write(f"Titulo: {tarefa["TITULO"]}")
    st.write(f"Descrição: {tarefa["DESCRICAO"]}")
    st.write(f"Prioridade: {tarefa["PRIORIDADE"]}")
    st.write(f"Status: {tarefa["STATUS"]}")
    st.write(f"Data De Criação: {tarefa["DATA_CRIACAO"]}")
    st.write(f"Data Prazo: {tarefa["DATA_VENCIMENTO"]}")
    st.write(f"Email: {tarefa["EMAIL"]}")
    
#Função para o botão apagar, onde o usuario poderá decidir se vai apagar a tarefa ou não
@st.dialog("Deseja Realmente Apagar a Tarefa?")
def apagar_tarefa(id):
    if st.button("Apagar"):
        apagar(id) 
        st.success("Tarefa deletada com sucesso.")
        time.sleep(1)
        st.rerun()
    if st.button("Voltar"):
        st.rerun()
        