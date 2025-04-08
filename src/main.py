from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List

# Conexão com o MongoDB
client = MongoClient("mongodb+srv://tmadm:kx3VIQZglRTRZprE@api-estacao.xikvdt1.mongodb.net/?retryWrites=true&w=majority")
db = client["api_estacao"]  # Nome do banco de dados
collection = db["dados_estacao"]  # Nome da coleção

app = FastAPI()

# Modelo para validar o JSON recebido
class Parametro(BaseModel):
    nome: str
    unidade: str
    valor: float

class Estacao(BaseModel):
    uuid: str

class DadosEstacao(BaseModel):
    estacao: Estacao
    parametros: List[Parametro]

@app.post("/dados/")
async def receber_dados(dados: DadosEstacao):
    try:
        # Converte os dados recebidos para um dicionário e insere no MongoDB
        collection.insert_one(dados.dict())
        return {"message": "Dados recebidos e armazenados com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar no banco de dados: {str(e)}")