import streamlit as st 
import pandas as pd
from modules.utils.utils import visualizar, pula_linha
from modules.dialogs.dialog import nova_tarefa, apagar_tarefa, infos_tarefa

#variaveis
lista_tarefas = visualizar()
lista_pendentes = []
lista_em_progresso = []
lista_concluidas = []
lista_baixa = []
lista_media = []
lista_alta = []
key_counter = 0
id = 0

#For para colocar valor nas listas requeridas
for tarefa in lista_tarefas:
    if tarefa['STATUS'] == 'pendente':
        lista_pendentes.append(tarefa)
    if tarefa['STATUS'] == 'em progresso':
        lista_em_progresso.append(tarefa)
    if tarefa['STATUS'] == 'concluido':
        lista_concluidas.append(tarefa)
    if tarefa['PRIORIDADE'] == 'baixa':
        lista_baixa.append(tarefa)
    if tarefa['PRIORIDADE'] == 'media':
        lista_media.append(tarefa)
    if tarefa['PRIORIDADE'] == 'alta':
        lista_alta.append(tarefa)

#DataFrames usados no relatorio
status_data1 = pd.DataFrame({
        'Pendentes': [len(lista_pendentes)],
        'Em Progresso': [len(lista_em_progresso)],
        'Concluido' : [len(lista_concluidas)]
        })

prioridade_data1 = pd.DataFrame({
        'Baixa': [len(lista_baixa)],
        'Media': [len(lista_media)],
        'Alta' : [len(lista_alta)]
        })

status_data2 = pd.DataFrame({
        'Quantidade': [len(lista_pendentes), len(lista_em_progresso), len(lista_concluidas)],
        'Tipos': ['Pendentes', 'Em Progresso', 'Concluido'],
        })

prioridade_data2 = pd.DataFrame({
        'Quantidade': [len(lista_baixa), len(lista_media), len(lista_alta)],
        'Tipos': ['baixa', 'media', 'alta'],
        })
        
cronograma_tarefas = pd.DataFrame({
    
})
#Relatorio que fica na pagina principal  
col1, col2 = st.columns(2)

#Coluna 1 com os dataFrames simples e titulos
with col1:
    st.header("Quantidade de Tarefas por status:")
    st.write(pd.DataFrame(status_data1))
    pula_linha(10)
    st.header("Quantidade de Tarefas por prioridade:")
    st.write(pd.DataFrame(prioridade_data1))

#Coluna 2 com os graficos
with col2:
    pula_linha(2)
    st.bar_chart(status_data2, x="Tipos", y="Quantidade",  color=(235,69,146))
    st.bar_chart(prioridade_data2, x="Tipos", y="Quantidade",  color=(235,69,146))

#SideBar onde se encontra a manipulaão do Crud e listagem das tarefas
with st.sidebar:
    st.image("./static/Img-Logo.png")
    st.title("Gerenciador de Tarefas")
    if st.button("Criar Nova Tarefa +"):
        nova_tarefa()
    tab1, tab2, tab3 = st.tabs(["Pendente", "Em progresso", "Concluido"])

    #Primeira vertente com tarefas pendentes
    with tab1:
        st.header("Tarefas Pendentes:")
        for tarefa in lista_pendentes:
            id = tarefa["ID"]
            with st.expander(tarefa["TITULO"]):
                key_counter += 1
                if st.button(label="Infos",key=key_counter):
                    infos_tarefa(id)
                key_counter += 1
                st.button(label="Atualizar", key=key_counter)
                key_counter += 1
                if st.button(label="Apagar",key=key_counter):
                    apagar_tarefa(id)
    
    #Segunda vertente com tarefas em processo
    with tab2:
        st.header("Tarefas Em Progresso:")
        for tarefa in lista_em_progresso:
            id = tarefa["ID"]
            with st.expander(tarefa["TITULO"]):
                key_counter += 1
                if st.button(label="Infos",key=key_counter):
                    infos_tarefa(id)
                key_counter += 1
                st.button(label="Atualizar", key=key_counter)
                key_counter += 1
                if st.button(label="Apagar",key=key_counter):
                    apagar_tarefa(id)
        
    #Terceira vertente com tareas concluidas
    with tab3:
        st.header("Tarefas Concluidas:")
        for tarefa in lista_concluidas:
            id = tarefa["ID"]
            with st.expander(tarefa["TITULO"]):
                key_counter += 1
                if st.button(label="Infos",key=key_counter):
                    infos_tarefa(id)
                key_counter += 1
                st.button(label="Atualizar", key=key_counter)
                key_counter += 1
                if st.button(label="Apagar",key=key_counter):
                    apagar_tarefa(id)

#-----------------------------------------------------------------------------------------------------------------------------------------------
# Codigo base Jennifer:
       
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


#-----------------------------------------------------------------------------------------------------------------------------------------------
#Codigo base Felipe:

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