🌍 [Leia em Português](README.pt-BR.md)

# Task Manager

Web application developed in python using  `streamlit` to manager task integrated with database(oracle) by api developed using `fastapi`.

## Technologies Used

- `fastapi` - Api development.
- `oracledb` - Connection with the database.
- `requests` - Make request to the api.
- `python-dotenv` - Get the environment variables.
- `streamlit` - Interface development.

## Features

- `Task Management`: Complete handling of tasks such as Create, Edit, Delete and List.
- `Oracle Database`: All information is stored and manipulated through a connection to OracleDB, ensuring data persistence and security.
- `Email notification system`: Receive notifications about your tasks in your email.
- `Report`: Report on the pending, in progress, and completed tasks.

## Steps to install and run

1. Clone the Repository:

```bash
git clone https://github.com/felipeclarindo/task-manager.git
```

2. Enter directory:

```bash
cd task-manager
```

3. Create `Virtual Environment`:

```bash
python -m venv .venv
```

4. Enable `Virtual Environment` by running the `.bat` file in `.venv/Scripts/activate.bat`.

5. Install dependencies :

```bash
pip install - r requirements.txt
```

6. Create the '.env' file based on the [.env.example](.env.example) for connection to the database.

7. Run the api server:

```bash
fastapi dev src/api/api.py
```

7. Run the application

```bash
streamlit run src/main.py
```

Não esqueça de conferir os caminhos (path), para rodar os comandos inicializando a aplicação da forma correta!

8. Don't forget to check the paths, to run the commands initializing the application correctly and check if the api is running as well when running the application!

## Contribution

Contributions are welcome! If you have suggestions for improvements, feel free to open an issue or submit a pull request.

## Author

**Felipe Clarindo**

- [LinkedIn](https://www.linkedin.com/in/felipeclarindo)
- [Instagram](https://www.instagram.com/lipethecoder)
- [GitHub](https://github.com/felipeclarindo)

## License

This project is licensed under the [GNU Affero License](https://www.gnu.org/licenses/agpl-3.0.html).
