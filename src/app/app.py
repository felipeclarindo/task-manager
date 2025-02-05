import streamlit as st
import pandas as pd
from .modules.utils.utils import visualizar, pula_linha, lista_cronograma
from .modules.dialogs.dialog import (
    nova_tarefa,
    apagar_tarefa,
    infos_tarefa,
    atualizar_tarefa,
    criar_planejamento,
)


class App:
    def __init__(self):
        self.tasks_list = visualizar()
        self.order_list = lista_cronograma(self.tasks_list)
        self.pending_list = []
        self.progress_list = []
        self.completed_list = []
        self.low_list = []
        self.mid_list = []
        self.high_list = []
        self.key_counter = 0
        self.id = 0

    def run(self):
        st.set_page_config(
            page_title="Task Manager",
            page_icon="./app/static/Img-Logo.png",
            layout="wide",
        )
        for task in self.tasks_list:
            if task["STATUS"] == "pendente":
                self.pending_list.append(task)
            if task["STATUS"] == "em progresso":
                self.progress_list.append(task)
            if task["STATUS"] == "concluido":
                self.completed_list.append(task)
            if task["PRIORIDADE"] == "baixa":
                self.low_list.append(task)
            if task["PRIORIDADE"] == "media":
                self.mid_list.append(task)
            if task["PRIORIDADE"] == "alta":
                self.high_list.append(task)

        # DataFrames usados no relatório
        status_data1 = pd.DataFrame(
            {
                "Pendentes": [len(self.pending_list)],
                "Em Progresso": [len(self.progress_list)],
                "Concluido": [len(self.completed_list)],
            }
        )

        prioridade_data1 = pd.DataFrame(
            {
                "Baixa": [len(self.low_list)],
                "Media": [len(self.mid_list)],
                "Alta": [len(self.high_list)],
            }
        )

        planejamento_data = pd.DataFrame(
            {
                "Titulo": [
                    tarefa["titulo"]
                    for tarefa in self.order_list
                    if tarefa["status"] != "concluido"
                ],
                "Status": [
                    tarefa["status"]
                    for tarefa in self.order_list
                    if tarefa["status"] != "concluido"
                ],
                "Prioridade": [
                    tarefa["prioridade"]
                    for tarefa in self.order_list
                    if tarefa["status"] != "concluido"
                ],
                "Dias Restantes": [
                    tarefa["dias para entrega"]
                    for tarefa in self.order_list
                    if tarefa["status"] != "concluido"
                ],
            }
        )

        status_data2 = pd.DataFrame(
            {
                "Quantidade": [
                    len(self.pending_list),
                    len(self.progress_list),
                    len(self.completed_list),
                ],
                "Tipos": ["Pendentes", "Em Progresso", "Concluido"],
            }
        )

        prioridade_data2 = pd.DataFrame(
            {
                "Quantidade": [
                    len(self.low_list),
                    len(self.mid_list),
                    len(self.high_list),
                ],
                "Tipos": ["baixa", "media", "alta"],
            }
        )

        # Relatório que fica na página principal
        col1, col2 = st.columns(2)

        # Coluna 1 com os dataFrames simples e títulos
        with col1:
            st.header("Quantidade de Tarefas por status:")
            st.write(pd.DataFrame(status_data1))
            pula_linha(10)
            st.header("Quantidade de Tarefas por prioridade:")
            st.write(pd.DataFrame(prioridade_data1))

        # Coluna 2 com os gráficos
        with col2:
            pula_linha(2)
            st.bar_chart(status_data2, x="Tipos", y="Quantidade", color=(235, 69, 146))
            st.bar_chart(
                prioridade_data2, x="Tipos", y="Quantidade", color=(235, 69, 146)
            )

        # SideBar onde se encontra a manipulação do Crud e listagem das tarefas
        with st.sidebar:
            st.image("./src/app/static/Img-Logo.png")
            st.title("Gerenciador de Tarefas")
            if st.button("Criar nova tarefa +"):
                nova_tarefa()
            if st.button("Criar planejamento"):
                criar_planejamento(planejamento_data)
            tab1, tab2, tab3 = st.tabs(["Pendente", "Em progresso", "Concluido"])

            # Primeira vertente com tarefas pendentes
            with tab1:
                st.header("Tarefas Pendentes:")
                for tarefa in self.pending_list:
                    id = tarefa["ID"]
                    with st.expander(tarefa["TITULO"]):
                        self.key_counter += 1
                        if st.button(label="Infos", key=self.key_counter):
                            infos_tarefa(id)
                        self.key_counter += 1
                        if st.button(label="Atualizar", key=self.key_counter):
                            atualizar_tarefa(id)
                        self.key_counter += 1
                        if st.button(label="Apagar", key=self.key_counter):
                            apagar_tarefa(id)

            # Segunda vertente com tarefas em progresso
            with tab2:
                st.header("Tarefas Em Progresso:")
                for tarefa in self.progress_list:
                    id = tarefa["ID"]
                    with st.expander(tarefa["TITULO"]):
                        self.key_counter += 1
                        if st.button(label="Infos", key=self.key_counter):
                            infos_tarefa(id)
                        self.key_counter += 1
                        if st.button(label="Atualizar", key=self.key_counter):
                            atualizar_tarefa(id)
                        self.key_counter += 1
                        if st.button(label="Apagar", key=self.key_counter):
                            apagar_tarefa(id)

            # Terceira vertente com tarefas concluídas
            with tab3:
                st.header("Tarefas Concluidas:")
                for tarefa in self.completed_list:
                    id = tarefa["ID"]
                    with st.expander(tarefa["TITULO"]):
                        self.key_counter += 1
                        if st.button(label="Infos", key=self.key_counter):
                            infos_tarefa(id)
                        self.key_counter += 1
                        if st.button(label="Atualizar", key=self.key_counter):
                            atualizar_tarefa(id)
                        self.key_counter += 1
                        if st.button(label="Apagar", key=self.key_counter):
                            apagar_tarefa(id)
