import httpx
import logging
from pymongo import MongoClient
from datetime import datetime
from .tipo_parametro_service import TipoParametroService

class DataSyncService:
    def __init__(self):
        # MongoDB connection
        self.client = MongoClient("mongodb+srv://tmadm:apifatec2025@api-estacao.xikvdt1.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["api_estacao"]
        self.collection = self.db["dados_estacao"]
        
        # Serviços
        self.tipo_parametro_service = TipoParametroService()
        
        # API config
        self.api_url = "http://localhost:3000/api/medidas"
        self.headers = {
            'Authorization': 'chave_fixa',
            'Content-Type': 'application/json'
        }

    async def sync_data(self):
        try:
            # Busca dados não processados do MongoDB
            dados_para_processar = self.collection.find({"processado": {"$ne": True}})
            
            async with httpx.AsyncClient() as client:
                for dados in dados_para_processar:
                    for parametro in dados["parametros"]:
                        # Busca o ID do tipo de parâmetro
                        id_parametro = await self.tipo_parametro_service.get_id_parametro(parametro["nome"])
                        
                        if id_parametro:
                            medida = {
                                "valor": parametro["valor"],
                                "unix_time": dados.get("unix_time", datetime.utcnow().isoformat()),
                                "estacao": {
                                    "uid": dados["estacao"]["uid"]
                                },
                                "parametro": {
                                    "id_parametro": id_parametro
                                }
                            }

                            # Envia para a API
                            response = await client.post(
                                self.api_url,
                                json=medida,
                                headers=self.headers
                            )

                            if response.status_code in [200, 201]:
                                # Marca como processado no MongoDB
                                self.collection.update_one(
                                    {"_id": dados["_id"]},
                                    {"$set": {"processado": True}}
                                )
                                logging.info(f"Dados processados para estação {dados['estacao']['uid']}")
                            else:
                                logging.error(f"Erro ao enviar dados: {response.status_code}")
                        else:
                            logging.error(f"Tipo de parâmetro não encontrado: {parametro['nome']}")

        except Exception as e:
            logging.error(f"Erro na sincronização: {str(e)}")