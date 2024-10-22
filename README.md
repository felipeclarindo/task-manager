# Task Manager

Gerenciador de tarefas desenvolvido em Python, para inserção e manipulação de dados (API).

## Funcionalidades

- **Criar Tarefas:** Permite a criação de novas tarefas com informações detalhadas, como título, descrição, data de vencimento e prioridade.

- **Atualizar Tarefas:** O sistema permite a edição das tarefas existentes, ajustando campos como descrição, status, prioridade ou outro que seja.

- **Excluir Tarefas:** Possibilidade de remover tarefas quando concluídas ou não mais necessárias.

- **Listagem de Tarefas:** Visualização de todas as tarefas criadas, filtradas por status, prioridade ou data.

- **Banco de Dados Oracle:** Todas as informações são armazenadas e manipuladas através de uma conexão com o OracleDB, garantindo persistência e segurança dos dados.

- **Sistema de notificação por email:** Receba no seu email as notificações sobre suas tarefas.

- **Relatório:** Relatório sobre as tarefas pendentes, em andamento e concluídas.

## Requisitos

- Python 3.x
- oracledb

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/felipeclarindo/task-manager.git
```

2. Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

3. Execute a API no terminal:

```bash
cd api
fastapi dev api.py
```

4. Execute a GUI em outro terminal:
```bash
cd app
streamlit run app.py
```
Não esqueça de trocar os caminhos (path), para rodar os comandos inicializando a aplicação

## Equipe

- Samir Hage Neto - **RM: 557260**
- Felipe Gabriel Lopes Pinheiro Clarindo - **RM: 554547**
- Jennifer Suzuki - **RM: 554661**
- Victor Augusto G. Fávaro - **RM: 555059**
- Felipe Levi Stephens Fidelix - **RM: 556426**
