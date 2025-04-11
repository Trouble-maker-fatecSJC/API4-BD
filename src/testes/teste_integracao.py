import requests
import json
from datetime import datetime

# Configurações
BASE_URL = "http://localhost:8000"
EXTERNAL_API = "http://localhost:3000"
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'chave_fixa'  # Adiciona o header de autorização
}

def test_send_data():
    print("\nTestando envio de dados...")
    
    test_data = {
        "estacao": {
            "uid": "bff1ec38-ed83-4f22-8bd6-5e8f4643cd24"
        },
        "parametros": [
            {
                "nome": "Chuva",
                "valor": 25.5
            },
            {
                "nome": "Direcao Vento",
                "valor": 65.0
            }
        ],
        "unix_time": 1596484800
    }

    response = requests.post(f"{BASE_URL}/dados/", json=test_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_sync_data():
    print("\nTestando sincronização...")
    
    # Aciona sincronização
    response = requests.post(f"{BASE_URL}/sync/process")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Verifica se os dados foram enviados para a API externa (agora com autorização)
    external_response = requests.get(f"{EXTERNAL_API}/api/medidas", headers=HEADERS)
    print("\nDados na API externa:")
    print(f"Status Code: {external_response.status_code}")
    if external_response.status_code == 200:
        medidas = external_response.json()
        print(f"Quantidade de medidas: {len(medidas)}")
        if len(medidas) > 0:
            print("Última medida:", json.dumps(medidas[-1], indent=2))
    else:
        print(f"Erro na API externa: {external_response.text}")

if __name__ == "__main__":
    print("Iniciando testes de integração...")
    test_send_data()
    test_sync_data()