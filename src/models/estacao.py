from pydantic import BaseModel, validator
from typing import List
from datetime import datetime
import pytz

class Parametro(BaseModel):
    nome: str
    valor: float

class Estacao(BaseModel):
    uid: str

class DadosEstacao(BaseModel):
    estacao: Estacao
    parametros: List[Parametro]
    unix_time: int

    @validator('unix_time')
    def convert_to_br_time(cls, v):
        # Convert Unix timestamp to datetime
        utc_time = datetime.fromtimestamp(v, tz=pytz.UTC)
        # Convert to Brazil timezone
        br_tz = pytz.timezone('America/Sao_Paulo')
        br_time = utc_time.astimezone(br_tz)
        return br_time