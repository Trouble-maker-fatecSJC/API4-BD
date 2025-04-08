import paho.mqtt.client as mqtt
import json
import time

# Configura o cliente MQTT
con = mqtt.Client()
con.connect("test.mosquitto.org", 1883, 60)

con.loop_start()

print("Running pub")

# Dados da estação para envio
dados = {
    "estacao": {
        "uuid": "123e4567-e89b-12d3-a456-426614174000"
    },
    "parametros": [
        {"nome": "direcao_vento", "unidade": "graus", "valor": 180},
        {"nome": "velocidade", "unidade": "m/s", "valor": 5.5},
        {"nome": "indice_pluviometrico", "unidade": "mm", "valor": 12.3},
        {"nome": "umidade", "unidade": "%", "valor": 65},
        {"nome": "temperatura", "unidade": "°C", "valor": 22.4},
        {"nome": "pressao", "unidade": "hPa", "valor": 1013.25}
    ]
}

# Publica os dados periodicamente
try:
    while True:
        # Converte os dados para JSON
        msg = json.dumps(dados)
        # Publica no tópico
        con.publish("api-fatec/estacao/dados/", msg)
        print(f"Mensagem publicada: {msg}")
        # Aguarda 5 segundos antes de enviar novamente
        time.sleep(5)
except KeyboardInterrupt:
    print("Encerrando publisher...")
    con.loop_stop()
    con.disconnect()