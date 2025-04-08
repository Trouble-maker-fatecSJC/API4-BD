from pydantic import BaseModel
from typing import List

class Parametro(BaseModel):
    nome: str
    unidade: str
    valor: float

class Estacao(BaseModel):
    uuid: str

class DadosEstacao(BaseModel):
    estacao: Estacao
    parametros: List[Parametro]