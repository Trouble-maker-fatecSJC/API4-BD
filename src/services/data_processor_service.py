import httpx
import logging
from datetime import datetime
from pymongo import MongoClient

class DataProcessorService:
    def __init__(self):
        self.base_url = "http://localhost:3000/api"
        self.headers = {
            'Authorization': 'chave_fixa',
            'Content-Type': 'application/json'
        }
        # Conexão MongoDB
        self.client = MongoClient("mongodb+srv://tmadm:apifatec2025@api-estacao.xikvdt1.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["api_estacao"]
        self.collection = self.db["dados_estacao"]

    async def process_and_send_data(self, dados_estacao):
        try:
            param_types = await self.get_parameter_types()
            
            async with httpx.AsyncClient() as client:
                success_count = 0
                
                for param in dados_estacao["parametros"]:
                    param_id = param_types.get(param["nome"])
                    
                    if param_id is None:
                        logging.error(f"Parameter type not found: {param['nome']}")
                        continue

                    medida = {
                        "valor": param["valor"],
                        "unix_time": dados_estacao.get("unix_time", datetime.utcnow().isoformat()),
                        "estacao": {
                            "uid": dados_estacao["estacao"]["uid"]
                        },
                        "parametro": {
                            "id_parametro": param_id
                        }
                    }

                    response = await client.post(
                        f"{self.base_url}/medidas",
                        json=medida,
                        headers=self.headers
                    )
                    
                    if response.status_code in [200, 201]:
                        success_count += 1
                        logging.info(f"Measure {param['nome']} sent successfully")
                        
                        # Atualiza o status no MongoDB
                        self.collection.update_one(
                            {"_id": dados_estacao["_id"]},
                            {"$set": {"processado": True}}
                        )
                    else:
                        logging.error(f"Error sending measure {param['nome']}: {response.status_code}")

                return success_count > 0

        except Exception as e:
            logging.error(f"Error processing and sending data: {str(e)}")
            return False