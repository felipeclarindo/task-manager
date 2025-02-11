import streamlit as st
from datetime import datetime
import requests
import json
import time
import pandas as pd
from ..utils.utils import criar_tarefa, vizualizar_tarefa, apagar, atualizar
from ..validations.validations import (
    validate_title,
    validate_desc,
    validate_prazo,
    validate_prioridade,
    validate_email,
)

# Funções dialog criam uma caixa de diálogo com o usuario


# Função para o botão nova tarefa, onde o usuário colocará as informações necessárias para criar uma nova tarefa
@st.dialog("Nova tarefa")
def nova_tarefa():
    titulo = st.text_input("Titulo: ", placeholder="Digite o título")
    descricao = st.text_input("Descrição: ", placeholder="Digite uma descrição")
    prioridade = st.selectbox(
        "Prioridade",
        ["baixa", "media", "alta"],
        index=None,
        placeholder="Escolha a prioridade desejada",
    )
    prazo = st.date_input("Prazo", datetime.today())
    diferença = prazo - datetime.today().date()
    prazo = diferença.days
    email = st.text_input("E-mail: ", placeholder="Digite seu e-mail")
    if st.button("Criar"):
        tarefa = {
            "titulo": titulo,
            "descricao": descricao,
            "prioridade": prioridade,
            "prazo": prazo,
            "email": email,
        }
        try:
            validate_title(titulo)
            validate_desc(descricao)
            validate_prioridade(prioridade)
            validate_prazo(prazo)
            validate_email(email)
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


# Função para o botão info, onde o usuário poderá ver todas as informações daquela tarefa
@st.dialog("Infos da tarefa")
def infos_tarefa(id: int):
    tarefa = vizualizar_tarefa(id)
    st.write(f"Titulo: {tarefa["TITULO"]}")
    st.write(f"Descrição: {tarefa["DESCRICAO"]}")
    st.write(f"Prioridade: {tarefa["PRIORIDADE"]}")
    st.write(f"Status: {tarefa["STATUS"]}")
    st.write(f"Data De Criação: {tarefa["DATA_CRIACAO"]}")
    st.write(f"Data Prazo: {tarefa["DATA_VENCIMENTO"]}")
    st.write(f"Email: {tarefa["EMAIL"]}")


# Função para o botão apagar, onde o usuário poderá decidir se vai apagar a tarefa ou não
@st.dialog("Deseja realmente apagar a tarefa?")
def apagar_tarefa(id):
    if st.button("Apagar"):
        apagar(id)
        st.success("Tarefa deletada com sucesso.")
        time.sleep(1)
        st.rerun()
    if st.button("Voltar"):
        st.rerun()


@st.dialog("Atualizar tarefa: ")
def atualizar_tarefa(id: int):
    lista_prioridade = ["baixa", "media", "alta"]
    lista_status = ["pendente", "em progresso", "concluido"]
    tarefa = vizualizar_tarefa(id)
    titulo = st.text_input("Titulo: ", value=tarefa["TITULO"])
    descricao = st.text_input("Descrição: ", value=tarefa["DESCRICAO"])
    prioridade = st.selectbox(
        "Prioridade",
        lista_prioridade,
        index=lista_prioridade.index(tarefa["PRIORIDADE"]),
    )
    status = st.selectbox(
        "Status", lista_status, index=lista_status.index(tarefa["STATUS"])
    )
    prazo = st.date_input(
        "Prazo", value=datetime.strptime(tarefa["DATA_VENCIMENTO"], "%d/%m/%Y").date()
    )
    diferença = prazo - datetime.today().date()
    prazo = diferença.days
    email = st.text_input("E-mail: ", value=tarefa["EMAIL"])
    if st.button("Atualizar"):
        tarefa = {
            "titulo": titulo,
            "descricao": descricao,
            "prioridade": prioridade,
            "prazo": prazo,
            "email": email,
            "status": status,
        }
        try:
            validate_title(titulo)
            validate_desc(descricao)
            validate_prioridade(prioridade)
            validate_prazo(prazo)
            validate_email(email)
            resposta_api = atualizar(id, json.dumps(tarefa))
            st.success(resposta_api["message"])
            time.sleep(1)
            st.rerun()
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 422:
                st.error("Erro de validação: os dados enviados não estão corretos.")
            else:
                st.error(f"Erro ao atualizar a tarefa: {err}")

            st.write("Resposta da API:", err.response.text)

        except json.JSONDecodeError:
            st.error("Erro ao processar a resposta da API. Resposta inválida.")

        except Exception as e:
            st.error(f"Ocorreu um erro inesperado: {e}")


@st.dialog("Planejamento:")
def criar_planejamento(data: pd.DataFrame):
    st.write(pd.DataFrame(data))
