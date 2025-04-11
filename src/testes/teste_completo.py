import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import time
import random
from services.data_processor_service import DataProcessorService
import asyncio

# Configurações
BASE_URL = "http://localhost:8000"
EXTERNAL_API = "http://localhost:3000"
HEADERS = {
    'Authorization': 'chave_fixa',
    'Content-Type': 'application/json'
}

def generate_test_data():
    return {
        "estacao": {
            "uid": "bff1ec38-ed83-4f22-8bd6-5e8f4643cd24"
        },
        "parametros": [
            {
                "nome": "Chuva",
                "valor": round(random.uniform(0, 100), 2)
            },
            {
                "nome": "Direcao Vento",
                "valor": round(random.uniform(0, 360), 2)
            }
        ],
        "unix_time": int(time.time())
    }

async def test_complete_flow():
    print("\n=== Iniciando Teste Completo ===")
    
    # 1. Teste de envio de dados
    print("\n1. Enviando dados para a API...")
    test_data = generate_test_data()
    print(f"Dados de teste: {test_data}")
    
    response = requests.post(f"{BASE_URL}/dados/", json=test_data)
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}")

    # 2. Aguarda processamento
    print("\n2. Aguardando processamento...")
    time.sleep(2)

    # 3. Teste de sincronização
    print("\n3. Testando sincronização...")
    sync_response = requests.post(f"{BASE_URL}/sync/process")
    print(f"Status sincronização: {sync_response.status_code}")
    print(f"Resposta sincronização: {sync_response.json()}")

    # 4. Verifica dados na API externa
    print("\n4. Verificando dados na API externa...")
    external_response = requests.get(f"{EXTERNAL_API}/api/medidas", headers=HEADERS)
    if external_response.status_code == 200:
        medidas = external_response.json()
        print(f"Quantidade de medidas: {len(medidas)}")
        if len(medidas) > 0:
            print("Última medida registrada:")
            print(f"Estação: {medidas[-1]['estacao']['uid']}")
            print(f"Valor: {medidas[-1]['valor']}")
            print(f"Data: {medidas[-1]['unix_time']}")
    else:
        print(f"Erro ao buscar medidas: {external_response.status_code}")

    print("\n=== Teste Completo Finalizado ===")

if __name__ == "__main__":
    asyncio.run(test_complete_flow())