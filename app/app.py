import streamlit as st 
import pandas as pd
from .modules.utils.utils import visualizar, pula_linha, lista_cronograma
from .modules.dialogs.dialog import nova_tarefa, apagar_tarefa, infos_tarefa, atualizar_tarefa, criar_planejamento

class App:
    def __init__(self):
        self.lista_tarefas = visualizar()
        self.lista_ordenada = lista_cronograma(self.lista_tarefas)
        self.lista_pendentes = []
        self.lista_em_progresso = []
        self.lista_concluidas = []
        self.lista_baixa = []
        self.lista_media = []
        self.lista_alta = []
        self.key_counter = 0
        self.id = 0

    def run(self):
        st.set_page_config(page_title="Task Manager", page_icon="./app/static/Img-Logo.png", layout="wide")
        #For para colocar valor nas listas requeridas
        for tarefa in self.lista_tarefas:
            if tarefa['STATUS'] == 'pendente':
                self.lista_pendentes.append(tarefa)
            if tarefa['STATUS'] == 'em progresso':
                self.lista_em_progresso.append(tarefa)
            if tarefa['STATUS'] == 'concluido':
                self.lista_concluidas.append(tarefa)
            if tarefa['PRIORIDADE'] == 'baixa':
                self.lista_baixa.append(tarefa)
            if tarefa['PRIORIDADE'] == 'media':
                self.lista_media.append(tarefa)
            if tarefa['PRIORIDADE'] == 'alta':
                self.lista_alta.append(tarefa)

        #DataFrames usados no relatório
        status_data1 = pd.DataFrame({
                'Pendentes': [len(self.lista_pendentes)],
                'Em Progresso': [len(self.lista_em_progresso)],
                'Concluido' : [len(self.lista_concluidas)]
                })

        prioridade_data1 = pd.DataFrame({
                'Baixa': [len(self.lista_baixa)],
                'Media': [len(self.lista_media)],
                'Alta' : [len(self.lista_alta)]
                })

        planejamento_data = pd.DataFrame({
                'Titulo': [tarefa["titulo"] for tarefa in self.lista_ordenada if tarefa["status"] != "concluido"],
                'Status': [tarefa["status"] for tarefa in self.lista_ordenada if tarefa["status"] != "concluido"],
                'Prioridade' : [tarefa["prioridade"] for tarefa in self.lista_ordenada if tarefa["status"] != "concluido"],
                'Dias Restantes': [tarefa["dias para entrega"] for tarefa in self.lista_ordenada if tarefa["status"] != "concluido"]
                })

        status_data2 = pd.DataFrame({
                'Quantidade': [len(self.lista_pendentes), len(self.lista_em_progresso), len(self.lista_concluidas)],
                'Tipos': ['Pendentes', 'Em Progresso', 'Concluido'],
                })

        prioridade_data2 = pd.DataFrame({
                'Quantidade': [len(self.lista_baixa), len(self.lista_media), len(self.lista_alta)],
                'Tipos': ['baixa', 'media', 'alta'],
                })
                
        #Relatório que fica na página principal  
        col1, col2 = st.columns(2)

        #Coluna 1 com os dataFrames simples e títulos
        with col1:
            st.header("Quantidade de Tarefas por status:")
            st.write(pd.DataFrame(status_data1))
            pula_linha(10)
            st.header("Quantidade de Tarefas por prioridade:")
            st.write(pd.DataFrame(prioridade_data1))

        #Coluna 2 com os gráficos
        with col2:
            pula_linha(2)
            st.bar_chart(status_data2, x="Tipos", y="Quantidade",  color=(235,69,146))
            st.bar_chart(prioridade_data2, x="Tipos", y="Quantidade",  color=(235,69,146))

        #SideBar onde se encontra a manipulação do Crud e listagem das tarefas
        with st.sidebar:
            st.image("./app/static/Img-Logo.png")
            st.title("Gerenciador de Tarefas")
            if st.button("Criar nova tarefa +"):
                nova_tarefa()
            if st.button("Criar planejamento"):
                criar_planejamento(planejamento_data)
            tab1, tab2, tab3 = st.tabs(["Pendente", "Em progresso", "Concluido"])

            #Primeira vertente com tarefas pendentes
            with tab1:
                st.header("Tarefas Pendentes:")
                for tarefa in self.lista_pendentes:
                    id = tarefa["ID"]
                    with st.expander(tarefa["TITULO"]):
                        self.key_counter += 1
                        if st.button(label="Infos",key=self.key_counter):
                            infos_tarefa(id)
                        self.key_counter += 1
                        if st.button(label="Atualizar", key=self.key_counter):
                            atualizar_tarefa(id)
                        self.key_counter += 1
                        if st.button(label="Apagar",key=self.key_counter):
                            apagar_tarefa(id)
            
            #Segunda vertente com tarefas em progresso
            with tab2:
                st.header("Tarefas Em Progresso:")
                for tarefa in self.lista_em_progresso:
                    id = tarefa["ID"]
                    with st.expander(tarefa["TITULO"]):
                        self.key_counter += 1
                        if st.button(label="Infos",key=self.key_counter):
                            infos_tarefa(id)
                        self.key_counter += 1
                        if st.button(label="Atualizar", key=self.key_counter):
                            atualizar_tarefa(id)
                        self.key_counter += 1
                        if st.button(label="Apagar",key=self.key_counter):
                            apagar_tarefa(id)
                
            #Terceira vertente com tarefas concluídas
            with tab3:
                st.header("Tarefas Concluidas:")
                for tarefa in self.lista_concluidas:
                    id = tarefa["ID"]
                    with st.expander(tarefa["TITULO"]):
                        self.key_counter += 1
                        if st.button(label="Infos",key=self.key_counter):
                            infos_tarefa(id)
                        self.key_counter += 1
                        if st.button(label="Atualizar", key=self.key_counter):
                            atualizar_tarefa(id)
                        self.key_counter += 1
                        if st.button(label="Apagar",key=self.key_counter):
                            apagar_tarefa(id)
