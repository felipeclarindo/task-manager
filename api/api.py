from fastapi import FastAPI
from .modules.database.models import Crud
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

class PostTask(BaseModel):
    titulo: str
    descricao: str
    prioridade: str
    prazo: int
    email: str

class PutTask(BaseModel):
    id: int
    titulo: str
    descricao: str
    prioridade: str
    prazo: int
    email: str

class PatchTask(BaseModel):
    id: int
    dado: str
    novo_dado: str

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
@app.get("/api")
async def index():
    return {"mensagem": "O Gerenciador de tarefas está online."}

# Criando rota de pegar dados
@app.get("/api/tasks")
async def get_all_tasks():
    response = crud.get_all()
    return response

# Criando rota de pegar dado com id
@app.get("/api/tasks/{id}")
async def get_task_with_id(id: int):
    response = crud.get_with_id(id)
    return response

# Criando rota de envio de dados
@app.post("/api/tasks")
async def post_task(data: PostTask):
    response = crud.post(data.titulo, data.prioridade, data.prazo, data.email)
    return response

# Criando rota de atualização de dados
@app.put("/api/tasks")
async def put_task(data: PutTask):
    response = crud.put(data.id, data.titulo, data.prioridade, data.prazo, data.email)
    return response

# Criando rota de atualização de um único dado
@app.patch("/api/tasks")
async def patch_task(data: PatchTask):
    response = crud.patch(data.id, data.dado, data.novo_dado)
    return response

# Criando rota de remoção de dado
@app.delete("/api/tasks/{id}")
async def delete_task(id: int):
    response = crud.delete(id)
    return response
