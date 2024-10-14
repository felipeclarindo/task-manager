from fastapi import FastAPI
from json import dumps
from .modules.database.models import Crud
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


class PostTask(BaseModel):
    titulo: str
    prioridade: str
    prazo: int


class PutTask(BaseModel):
    id: int
    titulo: str
    prioridade: str
    prazo: int


class PatchTask(BaseModel):
    id: int
    dado: str
    novo_dado: str


class GetTaskWithId(BaseModel):
    id: int


app = FastAPI()

crud = Crud()

origins = [
    "http://localhost:8000",
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
@app.get("/api/")
def index():
    return {"mensagem": "A api está online."}


@app.get("/api/tasks")
def tasks():
    return {
        "mensagem": "Gerenciador de tarefas",
        "rotas": [
            "/api/tasks/post",
            "/api/tasks/put",
            "/api/tasks/patch",
            "/api/tasks/delete/<id>",
            "/api/tasks/get",
            "/api/tasks/get-with-id/<id>",
        ],
    }


# Criando rota de envio de dados
@app.post("/api/tasks/post")
def post_task(data: PostTask):
    response = crud.post(data.titulo, data.prioridade, data.prazo)
    return dumps(response)


# Criando rota de atualização de dados
@app.put("/api/tasks/put")
def put_task(data: PutTask):
    response = crud.put(data.id, data.titulo, data.prioridade, data.prazo)
    return dumps(response)


# Criando rota de atualização de um unico dado
@app.patch("/api/tasks/patch")
def patch_task(data: PatchTask):
    response = crud.patch(data.id, data.dado, data.novo_dado)
    return dumps(response)


# Criando rota de removação de dado
@app.delete("/api/tasks/delete/{id}")
def delete_task(id: int):
    response = crud.delete(id)
    return dumps(response)


# Criando rota de pegar dados
@app.get("/api/tasks/get-all")
def get_all_tasks():
    response = crud.get_all()
    if response["status"] == "success":
        return dumps(response)
    else:
        return dumps(response)


# Criando rota de pegar dado com id
@app.get("/api/tasks/get-with-id/{id}")
def get_task_with_id(id: int):
    response = crud.get_with_id(id)
    return dumps(response)
