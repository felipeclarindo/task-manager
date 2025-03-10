from typing import Optional
from fastapi import FastAPI
from .modules.database.crud import Crud
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


class Task(BaseModel):
    """
    Task Model

    Args:
        BaseModel (_type_): _description_
    """

    titulo: str
    descricao: str
    prioridade: str
    prazo: int
    email: str


class TaskPut(BaseModel):
    """
    TaskPut Model

    Args:
        BaseModel (_type_): _description_
    """

    titulo: str
    descricao: str
    prioridade: str
    prazo: int
    email: str
    status: Optional[str] = None


app = FastAPI()
crud = Crud()

origins = [
    "http://localhost:8000",
    "http://localhost:8501",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Criando rota principal
@app.get("/api")
async def home():
    return {"mensagem": "O Gerenciador de tarefas está online."}


# Criando rota de pegar dados
@app.get("/api/tasks")
async def get_all_tasks():
    """
    Function to get all tasks

    Returns:
        _response:  Response from the database
    """
    response = crud.get_all()
    return response


# Criando rota de pegar dado com id
@app.get("/api/tasks/{id}")
async def get_task_by_id(id: int):
    response = crud.get_by_id(id)
    return response


# Criando rota de envio de dados
@app.post("/api/tasks")
async def post_task(body: Task):
    response = crud.post(
        body.titulo, body.descricao, body.prioridade, body.prazo, body.email
    )
    return response


# Criando rota de atualização de dados
@app.put("/api/tasks/{id}")
async def put_task(id: int, body: TaskPut):
    response = crud.put(
        id,
        body.titulo,
        body.descricao,
        body.prioridade,
        body.prazo,
        body.email,
        body.status,
    )
    return response


# Criando rota de remoção de dado
@app.delete("/api/tasks/{id}")
async def delete_task(id: int):
    response = crud.delete(id)
    return response
