import requests
import json

# API endpoint
url = "http://localhost:8000/dados/"

# Test data
test_data = {
    "estacao": {
        "uuid": "test-station-001"
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

# Send POST request
response = requests.post(url, json=test_data)
print("Status Code:", response.status_code)
print("Response:", response.json())