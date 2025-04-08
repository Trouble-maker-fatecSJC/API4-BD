import paho.mqtt.client as mqtt
import json
import logging
from models.estacao import DadosEstacao
from services.mongodb_service import MongoDBService

class MQTTService:
    def __init__(self):
        self.broker = "test.mosquitto.org"
        self.port = 1883
        self.topic = "api-fatec/estacao/dados/"
        self.client = mqtt.Client()
        self.mongodb_service = MongoDBService()
        
        self.client.on_message = self.on_message
        
    def on_message(self, client, userdata, message):
        try:
            payload = json.loads(message.payload.decode('utf-8'))
            logging.info(f"Mensagem recebida no tópico {message.topic}")
            dados = DadosEstacao(**payload)
            self.mongodb_service.retry_mongodb_insert(dados.dict())
        except Exception as e:
            logging.error(f"Erro ao processar mensagem MQTT: {str(e)}")

    def start(self):
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.subscribe(self.topic, qos=2)
            self.client.loop_forever()
        except Exception as e:
            logging.error(f"Erro na conexão MQTT: {str(e)}")

    def publish(self, data):
        return self.client.publish(self.topic, json.dumps(data), qos=2)