# from services.external_services import ExternalAPIService
# from pymongo import MongoClient
# import logging

# class MQTTService:
#     def __init__(self):
#         self.external_api = ExternalAPIService()
#         self.client = MongoClient("mongodb+srv://tmadm:apifatec2025@api-estacao.xikvdt1.mongodb.net/?retryWrites=true&w=majority")
#         self.db = self.client["api_estacao"]
#         self.collection = self.db["dados_estacao"]

#     async def process_message(self, dados):
#         try:
#             # Verifica se a estação existe na API externa
#             estacao_existe = await self.external_api.verify_station_exists(dados.estacao.uid)
            
#             if estacao_existe:
#                 # Salva no MongoDB
#                 self.collection.insert_one(dados.dict())
#                 logging.info(f"Dados da estação {dados.estacao.uid} salvos com sucesso")
#                 return True
#             else:
#                 logging.warning(f"Estação {dados.estacao.uid} não encontrada na API externa")
#                 return False
                
#         except Exception as e:
#             logging.error(f"Erro ao processar mensagem: {str(e)}")
#             raise Exception(f"Falha ao processar mensagem: {str(e)}")

#     def start(self):
#         logging.info("Serviço MQTT iniciado")



# from services.external_services import ExternalAPIService
# from services.data_processor_service import DataProcessorService
# from pymongo import MongoClient
# import logging

# class MQTTService:
#     def __init__(self):
#         self.external_api = ExternalAPIService()
#         self.data_processor = DataProcessorService()
#         self.client = MongoClient("mongodb+srv://tmadm:apifatec2025@api-estacao.xikvdt1.mongodb.net/?retryWrites=true&w=majority")
#         self.db = self.client["api_estacao"]
#         self.collection = self.db["dados_estacao"]

#     async def process_message(self, dados):
#         try:
#             # Verifica se a estação existe
#             estacao_existe = await self.external_api.verify_station_exists(dados.estacao.uid)
            
#             if estacao_existe:
#                 # Salva no MongoDB
#                 dados_dict = dados.dict()
#                 self.collection.insert_one(dados_dict)
                
#                 # Processa e envia para a API externa
#                 await self.data_processor.process_and_send_data(dados_dict)
                
#                 logging.info(f"Dados da estação {dados.estacao.uid} processados e enviados")
#                 return True
#             else:
#                 logging.warning(f"Estação {dados.estacao.uid} não encontrada")
#                 return False
                
#         except Exception as e:
#             logging.error(f"Erro ao processar mensagem: {str(e)}")
#             raise Exception(f"Falha ao processar mensagem: {str(e)}")



from services.external_services import ExternalAPIService
from pymongo import MongoClient
import logging
import paho.mqtt.client as mqtt
import json
from models.estacao import DadosEstacao

class MQTTService:
    def __init__(self):
        # Serviços e conexões
        self.external_api = ExternalAPIService()
        self.client = MongoClient("mongodb+srv://tmadm:apifatec2025@api-estacao.xikvdt1.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["api_estacao"]
        self.collection = self.db["dados_estacao"]
        
        # Configurações MQTT
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_connect = self.on_connect
        
    def on_connect(self, client, userdata, flags, rc):
        logging.info(f"Conectado ao broker MQTT com código: {rc}")
        client.subscribe("api-fatec/estacao/dados/")
        
    def on_message(self, client, userdata, message):
        try:
            payload = json.loads(message.payload.decode('utf-8'))
            logging.info("Mensagem MQTT recebida")
            dados = DadosEstacao(**payload)
            self.process_message(dados)
        except Exception as e:
            logging.error(f"Erro ao processar mensagem MQTT: {str(e)}")
            
    async def process_message(self, dados):
        try:
            # Verifica se a estação existe
            estacao_existe = await self.external_api.verify_station_exists(dados.estacao.uid)
            
            if estacao_existe:
                # Salva no MongoDB
                dados_dict = dados.dict()
                dados_dict["processado"] = False  # Marca para processamento posterior
                self.collection.insert_one(dados_dict)
                logging.info(f"Dados da estação {dados.estacao.uid} salvos com sucesso")
                return True
            else:
                logging.warning(f"Estação {dados.estacao.uid} não encontrada")
                return False
                
        except Exception as e:
            logging.error(f"Erro ao processar mensagem: {str(e)}")
            raise Exception(f"Falha ao processar mensagem: {str(e)}")
            
    def start(self):
        try:
            logging.info("Iniciando serviço MQTT...")
            self.mqtt_client.connect("test.mosquitto.org", 1883, 60)
            self.mqtt_client.loop_forever()
        except Exception as e:
            logging.error(f"Erro ao iniciar serviço MQTT: {str(e)}")