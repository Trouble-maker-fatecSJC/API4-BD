from pymongo import MongoClient
import requests
import time
import random

# API endpoints
base_url = "http://localhost:8000"
dados_url = f"{base_url}/dados/"

# MongoDB connection
client = MongoClient("mongodb+srv://tmadm:apifatec2025@api-estacao.xikvdt1.mongodb.net/?retryWrites=true&w=majority")
db = client["api_estacao"]
collection = db["dados_estacao"]
failed_messages = db["failed_messages"]

def generate_test_data(with_error=False):
    data = {
        "estacao": {
            "uuid": f"test-station-{random.randint(1, 1000)}"
        },
        "parametros": [
            {
                "nome": "temperatura",
                "unidade": "°C",
                "valor": random.uniform(20, 30)
            }
        ]
    }
    
    # Introduce invalid data to force an error
    if with_error:
        data["parametros"][0]["valor"] = "invalid_value"
    
    return data

def test_successful_scenario():
    print("\nTesting successful scenario...")
    response = requests.post(dados_url, json=generate_test_data())
    print(f"Response: {response.json()}")
    time.sleep(2)  # Wait for MQTT processing

def test_error_scenario():
    print("\nTesting error scenario...")
    response = requests.post(dados_url, json=generate_test_data(with_error=True))
    print(f"Response: {response.json()}")
    time.sleep(2)  # Wait for MQTT processing

def check_results():
    print("\nChecking MongoDB results...")
    
    # Check last successful message
    last_message = collection.find_one(sort=[('_id', -1)])
    print("\nLast successful message:")
    print(last_message)
    
    # Check failed messages
    failed = list(failed_messages.find())
    print(f"\nFailed messages count: {len(failed)}")
    for msg in failed:
        print(f"Failed message: {msg}")

if __name__ == "__main__":
    # Clear previous test data
    failed_messages.delete_many({})
    
    # Run tests
    test_successful_scenario()
    test_error_scenario()
    test_error_scenario()
    
    # Check results
    check_results()