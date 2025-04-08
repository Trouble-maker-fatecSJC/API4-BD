from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List
import paho.mqtt.client as mqtt
import json
import threading
import logging
from datetime import datetime
import time

# Configuração do logging
logging.basicConfig(
    filename='api_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Conexão com o MongoDB
client = MongoClient("mongodb+srv://tmadm:apifatec2025@api-estacao.xikvdt1.mongodb.net/?retryWrites=true&w=majority")
db = client["api_estacao"]
collection = db["dados_estacao"]
failed_messages = db["failed_messages"]  # Nova coleção para mensagens com falha

app = FastAPI()

# Configurações MQTT
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "api-fatec/estacao/dados/"

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

def retry_mongodb_insert(data, max_retries=3, delay=1):
    for attempt in range(max_retries):
        try:
            collection.insert_one(data)
            logging.info(f"Dados salvos no MongoDB com sucesso após {attempt + 1} tentativa(s)")
            return True
        except Exception as e:
            logging.error(f"Tentativa {attempt + 1} falhou: {str(e)}")
            time.sleep(delay)
    
    # Se todas as tentativas falharem, salva na coleção de falhas
    failed_messages.insert_one({
        "data": data,
        "timestamp": datetime.utcnow(),
        "error_count": max_retries
    })
    logging.error("Todas as tentativas falharam. Mensagem salva em failed_messages")
    return False

# Callback quando mensagem MQTT é recebida
def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode('utf-8'))
        logging.info(f"Mensagem recebida no tópico {message.topic}")
        dados = DadosEstacao(**payload)
        retry_mongodb_insert(dados.dict())
    except Exception as e:
        logging.error(f"Erro ao processar mensagem MQTT: {str(e)}")

# Configuração do cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message

def start_mqtt():
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.subscribe(MQTT_TOPIC, qos=2)  # QoS 2 para garantir entrega única
        mqtt_client.loop_forever()
    except Exception as e:
        logging.error(f"Erro na conexão MQTT: {str(e)}")

# Inicia o cliente MQTT em uma thread separada
mqtt_thread = threading.Thread(target=start_mqtt)
mqtt_thread.daemon = True
mqtt_thread.start()

@app.post("/dados/")
async def receber_dados(dados: DadosEstacao):
    try:
        # Publica os dados no tópico MQTT com QoS 2
        mqtt_client.publish(MQTT_TOPIC, json.dumps(dados.dict()), qos=2)
        logging.info("Dados enviados para processamento via MQTT")
        return {"message": "Dados enviados para processamento!"}
    except Exception as e:
        logging.error(f"Erro ao processar dados: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar dados: {str(e)}")

# Endpoint para verificar mensagens com falha
@app.get("/failed-messages/")
async def get_failed_messages():
    failed = list(failed_messages.find({}, {'_id': 0}))
    return {"failed_messages": failed}