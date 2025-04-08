from pymongo import MongoClient
import json

# Conexão com o MongoDB
client = MongoClient("mongodb+srv://tmadm:apifatec2025@api-estacao.xikvdt1.mongodb.net/?retryWrites=true&w=majority")
db = client["api_estacao"]
collection = db["dados_estacao"]

# Busca o último registro
ultimo_dado = collection.find_one(sort=[('_id', -1)])
print("Último dado salvo no MongoDB:")
print(json.dumps(ultimo_dado, indent=2, default=str))