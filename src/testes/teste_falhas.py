from pymongo import MongoClient
import requests
import time
import random

# API endpoints
base_url = "http://localhost:8000"
dados_url = f"{base_url}/dados/"

# Conexão MongoDB
client = MongoClient("mongodb+srv://tmadm:apifatec2025@api-estacao.xikvdt1.mongodb.net/?retryWrites=true&w=majority")
db = client["api_estacao"]
collection = db["dados_estacao"]
failed_messages = db["failed_messages"]

def generate_test_data(with_error=False):
    data = {
        "estacao": {
            "uid": "bff1ec38-ed83-4f22-8bd6-5e8f4643cd24"
        },
        "parametros": [
            {
                "nome": "Chuva",
                "valor": round(random.uniform(0, 100), 2)  # Chuva entre 0 e 100mm
            },
            {
                "nome": "Direcao Vento",
                "valor": round(random.uniform(0, 360), 2)  # Direção do vento entre 0 e 360 graus
            }
        ],
        "unix_time": int(time.time())  # Timestamp atual
    }
    
    # Introduz dados inválidos para forçar erro
    if with_error:
        data["parametros"][0]["valor"] = "valor_invalido"
        data["parametros"][1]["valor"] = "valor_invalido"
    
    return data

def test_successful_scenario():
    print("\nTestando cenário de sucesso...")
    response = requests.post(dados_url, json=generate_test_data())
    print(f"Resposta: {response.json()}")
    time.sleep(2)  # Aguarda processamento

def test_error_scenario():
    print("\nTestando cenário de erro...")
    response = requests.post(dados_url, json=generate_test_data(with_error=True))
    print(f"Resposta: {response.json()}")
    time.sleep(2)  # Aguarda processamento

def check_results():
    print("\nVerificando resultados no MongoDB...")
    
    # Verifica última mensagem com sucesso
    last_message = collection.find_one(sort=[('_id', -1)])
    print("\nÚltima mensagem com sucesso:")
    print(last_message)
    
    # Verifica mensagens com falha
    failed = list(failed_messages.find())
    print(f"\nQuantidade de mensagens com falha: {len(failed)}")
    for msg in failed:
        print(f"Mensagem com falha: {msg}")

if __name__ == "__main__":
    # Limpa dados de teste anteriores
    failed_messages.delete_many({})
    
    # Executa testes
    test_successful_scenario()
    test_error_scenario()
    test_successful_scenario()
    
    # Verifica resultados
    check_results()