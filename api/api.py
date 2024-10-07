from fastapi import FastAPI
from json import dumps
from .modules.database.models import Crud
from pydantic import BaseModel

app = FastAPI()

crud = Crud()


class PostTask(BaseModel):
    titulo: str
    prioridade: str
    prazo: str


class PutTask(BaseModel):
    id: int
    titulo: str
    prioridade: str
    prazo: str


class PatchTask(BaseModel):
    id: int
    dado: str
    novo_dado: str


class DeleteTask(BaseModel):
    id: int


class GetTaskWithId(BaseModel):
    id: int


# Criando rota principal
@app.get("/")
def index():
    return {"mensagem": "A api está online."}


# Criando rota de envio de dados
@app.post("/tasks/post", METHODS=["POST"])
def post_task(data: PostTask):
    response = crud.post(data.titulo, data.prioridade, data.prazo)
    if response["status"] == "succes":
        return dumps({"message": "Dados inseridos no banco de dados com sucesso!"})
    else:
        return dumps({"message": response["message"]})


# Criando rota de atualização de dados
@app.put("/tasks/put", METHODS=["PUT"])
def put_task(data: PutTask):
    response = crud.put(data.id, data.titulo, data.prioridade, data.prazo)
    if response["status"] == "success":
        return dumps({"message": "Dados atualizado com sucesso"})
    else:
        return dumps({"message": response["message"]})


# Criando rota de atualização de um unico dado
@app.patch("/tasks/patch", METHODS=["PATCH"])
def patch_task(data: PatchTask):
    response = crud.patch(data.id, data.dado, data.novo_dado)
    if response["status"] == "succes":
        return dumps({"message": "Dado atualizados com sucesso"})
    else:
        return dumps({"message": response["message"]})


# Criando rota de removação de dado
@app.delete("/tasks/delete", METHODS=["DELETE"])
def delete_task(data: DeleteTask):
    response = crud.delete(data.id)
    if response["status"] == "success":
        return dumps({"message": "Registro deletado com sucesso!"})
    else:
        return dumps({"message": response["message"]})


# Criando rota de pegar dados
@app.get("/tasks/get", METHODS=["GET"])
def get_tasks():
    response = crud.get()
    if response["status"] == "success":
        return dumps({"message": response["message"]})
    else:
        return dumps({"message": response["message"]})


# Criando rota de pegar dado com id
@app.get("/tasks/get-with-id", METHODS=["GET"])
def get_task_with_id(data: GetTaskWithId):
    response = crud.get_with_id(data.id)
    if response["status"] == "succes":
        return dumps({"message": response["message"]})
    else:
        return dumps({"message": response["message"]})
