🌍 [Read in English](README.md)

# Task Manager

Aplicação Web desenvolvido em Python com `streamlit` para gerenciamento de tarefas integrado com banco de dados(oracle) via api desenvolvida em `fastapi`.

# Tecnologias Utilizadas

- `fastapi` - Desenvolvimento da api.
- `oracledb` - Conexão com o banco de dados.
- `requests` - Realizar a interação com a api.
- `python-dotenv` - Captura das variaveis de ambientes.
- `streamlit` - Desenvolvimento da Interface.

## Funcionalidades

- `Gerenciamento das tarefas`: Manipulação completa das tarefas como Criar, Editar, Deletar e Listar.
- `Banco de Dados Oracle`: Todas as informações são armazenadas e manipuladas através de uma conexão com o OracleDB, garantindo persistência e segurança dos dados.
- `Sistema de notificação por email`: Receba no seu email as notificações sobre suas tarefas.
- `Relatório`: Relatório sobre as tarefas pendentes, em andamento e concluídas.

## Passos para instalação e executação

1. Clone o repositório:

```bash
git clone https://github.com/felipeclarindo/task-manager.git
```

2. Entre no diretório:

```bash
cd task-manager
```

3. Crie o `Ambiente Virtual`:

```bash
python -m venv .venv
```

4. Ative o `Ambiente Virtual` executando o arquivo `.bat` em `caminho`.

5. Instale as dependências:

```bash
pip install -r requirements.txt
```

6. Crie o arquivo `.env` baseado no [.env.example](.env.example) para conexão com o banco de dados.

7. Execute o servidor da api:

```bash
fastapi dev src/api/api.py
```

7. Execute a aplicação:

```bash
streamlit run src/main.py
```

8. Não esqueça de conferir os caminhos (path), para rodar os comandos inicializando a aplicação da forma correta e verificar se a api está sendo executada também quando rodar a aplicação!

## Contribuição

Contribuições são bem-vindas! Se você tiver sugestões de melhorias, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Autor

**Felipe Clarindo**

- [LinkedIn](https://www.linkedin.com/in/felipeclarindo)
- [Instagram](https://www.instagram.com/lipethecoder)
- [GitHub](https://github.com/felipeclarindo)

## Licença

Este projeto está licenciado sob a [GNU Affero License](https://www.gnu.org/licenses/agpl-3.0.html).
