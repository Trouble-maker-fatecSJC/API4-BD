import requests
import time

# API endpoints
base_url = "http://localhost:8000"
dados_url = f"{base_url}/dados/"
failed_messages_url = f"{base_url}/failed-messages/"

# Dados de teste
test_data = {
    "estacao": {
        "uuid": "estacao-teste-001"
    },
    "parametros": [
        {
            "nome": "temperatura",
            "unidade": "°C",
            "valor": 25.5
        },
        {
            "nome": "umidade",
            "unidade": "%",
            "valor": 65.0
        }
    ]
}

def test_api():
    print("\n1. Enviando dados para a API...")
    response = requests.post(dados_url, json=test_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    # Aguarda um momento para o processamento MQTT
    print("\n2. Aguardando processamento MQTT...")
    time.sleep(2)

    # Verifica mensagens com falha
    print("\n3. Verificando mensagens com falha...")
    failed = requests.get(failed_messages_url)
    print(f"Failed messages: {failed.json()}")

if __name__ == "__main__":
    test_api()