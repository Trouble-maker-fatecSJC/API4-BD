import requests
import json

# API endpoint
url = "http://localhost:8000/dados/"  # Corrigido o endpoint

# Test data
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

# Send POST request
response = requests.post(url, json=test_data)
print("Status Code:", response.status_code)
print("Response:", response.json())