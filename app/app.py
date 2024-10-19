# from os import name, system
# from .modules.operations.atualizar import _atualizar
# from .modules.operations.remover import _remover
# from .modules.operations.adicionar import _adicionar
# from .modules.operations.visualizar import _visualizar

# class App:
#     def __init__(self) -> None:
#         pass

#     def clear(self) -> None:
#         if name == "nt":
#             system("cls")
#         else:
#             system("clear")

#     def menu(self):
#         self.clear()
#         print("-" * 40)
#         print("--------- Task Manager --------")
#         print("-" * 40)
#         print("1 - Adicionar Tarefa.")
#         print("2 - Atualizar Tarefa.")
#         print("3 - Remover Tarefa.")
#         print("4 - Ver Tarefas")
#         print("5 - Sair")

#     def adicionar_tarefa(self):
#         _adicionar()

#     def atualizar_tarefa(self):
#         _atualizar()

#     def remover_tarefa(self):
#         _remover()

#     def visualizar_tarefas(self):
#         _visualizar()

#     def run(self):
#         sair = False
#         while not sair:
#             self.menu()
#             option = str(input("Informe uma opção: "))
#             match option:
#                 case "1":
#                     self.adicionar_tarefa()
#                 case "2":
#                     self.atualizar_tarefa()
#                 case "3":
#                     self.remover_tarefa()
#                 case "4":
#                     self.visualizar_tarefas()
#                 case "5":
#                     saida_valida = False
#                     while not saida_valida:
#                         self.menu()

#                 case _:
#                     print("Opção ínvalida.")

import streamlit as st 
from datetime import datetime 
import requests
import json
# class Tarefa: 
#     def __init__(self, id, descricao, prioridade, prazo): 
#         self.id = id 
#         self.descricao = descricao 
#         self.prioridade = prioridade 
#         self.prazo = prazo 
#         self.status = 'pendente' 
        
# class GerenciadorTarefas: 
#     def __init__(self): 
#         self.tarefas = [] 
#         self.next_id = 1 
        
#     def adicionar_tarefa(self, descricao, prioridade, prazo): 
#         nova_tarefa = Tarefa(self.next_id, descricao, prioridade, prazo) 
#         self.tarefas.append(nova_tarefa) 
#         self.next_id += 1 
#         return nova_tarefa 
    
#     def relatorios(self): 
#         pendentes = [tarefa for tarefa in self.tarefas if tarefa.status == 'pendente'] 
#         em_andamento = [tarefa for tarefa in self.tarefas if tarefa.status == 'em andamento'] 
#         concluídas = [tarefa for tarefa in self.tarefas if tarefa.status == 'concluída'] 
#         return { 'pendentes': pendentes, 'em_andamento': em_andamento, 'concluídas': concluídas } 
    
# gerenciador = GerenciadorTarefas() 
# st.title("Gerenciador de Tarefas") 
# with st.form(key='form_tarefa'): 
#     descricao = st.text_input("Descrição da Tarefa") 
#     prioridade = st.selectbox("Prioridade", [1, 2, 3, 4, 5]) 
#     prazo = st.date_input("Prazo", datetime.today()) 
#     submit_button = st.form_submit_button("Adicionar Tarefa") 
#     if submit_button: 
#         gerenciador.adicionar_tarefa(descricao, prioridade, prazo) 
#         st.success("Tarefa adicionada com sucesso!") 
        
# # Relatórios 
# st.header("Relatórios") 
# relatorios = gerenciador.relatorios() 
# st.subheader("Tarefas Pendentes") 
# for tarefa in relatorios['pendentes']:
#     st.write(f"{tarefa.id} - {tarefa.descricao} | Prioridade: {tarefa.prioridade} | Prazo: {tarefa.prazo} | Status: {tarefa.status}") 
#     st.subheader("Tarefas em Andamento") 
# for tarefa in relatorios['em_andamento']: 
#     st.write(f"{tarefa.id} - {tarefa.descricao} | Prioridade: {tarefa.prioridade} | Prazo: {tarefa.prazo} | Status: {tarefa.status}") 
#     st.subheader("Tarefas Concluídas") 
# for tarefa in relatorios['concluídas']: 
#     st.write(f"{tarefa.id} - {tarefa.descricao} | Prioridade: {tarefa.prioridade} | Prazo: {tarefa.prazo} | Status: {tarefa.status}")

def visualizar():
    url = " http://127.0.0.1:8000/api/tasks/"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return json.loads(data['response'])
    

def vizualizar_tarefa(id):
    url = f" http://127.0.0.1:8000/api/tasks/{id}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    dict_data = json.loads(data)
    return json.loads(dict_data['response'])

def apagar(id):
    url = f" http://127.0.0.1:8000/api/tasks/{id}"
    response = requests.delete(url)
    response.raise_for_status()
    resposta = json.loads(response.json())["message"]
    return resposta
    

@st.dialog("Nova Tarefa")
def nova_tarefa():
    titulo = st.text_input("Titulo: ")
    prioridade = st.selectbox("Prioridade", ["baixa", "media", "média", "alta"]) 
    prazo = st.date_input("Prazo", datetime.today()) 
    status = "pendente"
    if st.button("Criar"):
        st.session_state.tarefa = {"titulo": titulo,"prioridade": prioridade, "status": status,"data_vencimento": prazo,"data_criacao": datetime.today()}
        st.rerun()

@st.dialog("Infos Da Tarefa")
def ifos_tarefa(id):
    tarefa = vizualizar_tarefa(id)
    st.write(f"Titulo: {tarefa["TITULO"]}")
    st.write(f"Descrição: {tarefa["DESCRICAO"]}")
    st.write(f"Prioridade: {tarefa["PRIORIDADE"]}")
    st.write(f"Status: {tarefa["STATUS"]}")
    st.write(f"Data De Criação: {tarefa["DATA_CRIACAO"]}")
    st.write(f"Data Prazo: {tarefa["DATA_VENCIMENTO"]}")
    st.write(f"Email: {tarefa["EMAIL"]}")
    

lista_tarefas = visualizar()
lista_pendentes = []
lista_em_progresso = []
lista_concluidas = []
key_counter = 0
id = 0

for tarefa in lista_tarefas:
    # if tarefa['STATUS'] == 'pendente':
    #     lista_pendentes.append(tarefa)
    # if tarefa['STATUS'] == 'em progresso':
    #     lista_em_progresso.append(tarefa)
    # if tarefa['STATUS'] == 'concluido':
    #     lista_concluidas.append(tarefa)
    print(lista_tarefas)

with st.sidebar:
    st.image("./static/Img-Logo.png", width=300)
    st.title("Gerenciador de Tarefas")
    if st.button("Criar Nova Tarefa +"):
        nova_tarefa()
    tab1, tab2, tab3 = st.tabs(["Pendente", "Em progresso", "Concluido"])
    col1, col2, col3 = st.columns(3)

    with tab1:
        st.header("Tarefas Pendentes:")
        for tarefa in lista_pendentes:
            id = tarefa["ID"]
            with st.expander(tarefa["TITULO"]):
                key_counter += 1
                if st.button(label="Infos",key=key_counter):
                    ifos_tarefa(id)
                key_counter += 1
                st.button(label="Atualizar", key=key_counter)
                key_counter += 1
                if st.button(label="Apagar",key=key_counter):
                    if apagar(id) == "Tarefa deletada com sucesso.":
                        st.success("Tarefa deletada com sucesso.")
                    else:
                        st.error(apagar(id))
        
    with tab2:
        st.header("Tarefas Em Progresso:")
        for tarefa in lista_em_progresso:
            id = tarefa["ID"]
            with st.expander(tarefa["TITULO"]):
                key_counter += 1
                if st.button(label="Infos",key=key_counter):
                    ifos_tarefa(id)
                key_counter += 1
                st.button(label="Atualizar", key=key_counter)
                key_counter += 1
                if st.button(label="Apagar",key=key_counter):
                    if apagar(id) == "Tarefa deletada com sucesso.":
                        st.success("Tarefa deletada com sucesso.")
                    else:
                        st.error(apagar(id))
        
        
    with tab3:
        st.header("Tarefas Concluidas:")
        for tarefa in lista_concluidas:
            id = tarefa["ID"]
            with st.expander(tarefa["TITULO"]):
                key_counter += 1
                if st.button(label="Infos",key=key_counter):
                    ifos_tarefa(id)
                key_counter += 1
                st.button(label="Atualizar", key=key_counter)
                key_counter += 1
                if st.button(label="Apagar",key=key_counter):
                    if apagar(id) == "Tarefa deletada com sucesso.":
                        st.success("Tarefa deletada com sucesso.")
                    else:
                        st.error(apagar(id))
        
