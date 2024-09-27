from fastapi import FastAPI
from requests import request
from json import dumps
from modules.models import Crud
from pydantic import BaseModel

app = FastAPI()

crud = Crud()


class PostTask(BaseModel):
    titulo: str
    prioridade: str
    status: str

class 



# Criando rota principal
@app.get("/")
def index():
    return {"mensagem": "A api está online."}


# Criando rota de envio de dados
@app.get("/tasks/post", methods=["POST"])
def post_task(data: PostTask):
    response = crud.post(data.titulo, data.prioridade, data.status)
    if response["status"] == "succes":
        return dumps({"message": "Dados inseridos no banco de dados com sucesso!"})
    else:
        return dumps({"message": "404"})


# Criando rota de atualização de dados
@app.get("/task/put", methods=["PUT"])
def put_task():
    data = request.json
    id = data.get("id")
    titulo = data.get("titulo")
    data_vencimento = data.get("data_vencimento")
    prioridade = data.get("prioridade")
    status = data.get("status")
    data_criacao = data.get("criacao")
    response = crud.put(id, titulo, data_vencimento, prioridade, status, data_criacao)
    if response["status"] == "success":
        return dumps({"message": "Dados atualizado com sucesso"})
    else:
        return dumps({"message": "404"})


# Criando rota de atualização de um unico dado
@app.get("/task/patch", methods=["PATCH"])
def patch_task(id: int, dado: str, novo_dado: str):
    response = crud.patch(id, dado, novo_dado)
    if response["status"] == "succes":
        return dumps({"message": "Dado atualizados com sucesso"})
    else:
        return dumps({"message": "404"})


# Criando rota de removação de dado
@app.get("/task/delete", metods=["DELETE"])
def delete_task(id: int):
    deleted = crud.delete(id)
    if deleted["status"] == "success":
        return dumps({"message": "Registro deletado com sucesso!"})
    else:
        return dumps({"message": "404"})


# Criando rota de pegar dados
@app.get("/task/get", methods=["GET"])
def get_tasks():
    response = crud.get()
    if response["status"] == "success":
        return dumps({"message": response["message"]})
    else:
        return dumps({"message": "404"})


# Criando rota de pegar dado com id
@app.get("/tasks/get-with-id", methods=["GET"])
def get_tasks_with_id(id: int):
    response = crud.get_with_id(id)
    if response["status"] == "succes":
        return dumps({"message": response["message"]})
    else:
        return dumps({"message": "404"})
