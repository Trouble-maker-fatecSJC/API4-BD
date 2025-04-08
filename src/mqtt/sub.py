import paho.mqtt.client as mqtt
import json  # Importa o módulo para manipular JSON

def on_connect(con, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    con.subscribe("api-fatec/estacao/dados/")  # Inscreve-se no tópico

def on_message(con, userdata, msg):
    try:
        # Decodifica a mensagem recebida como JSON
        payload = json.loads(msg.payload.decode('utf-8'))
        print(f"Mensagem recebida no tópico {msg.topic}: {payload}")
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON: {msg.payload}")

print("Running sub")
con = mqtt.Client()
con.on_connect = on_connect
con.on_message = on_message

con.connect("test.mosquitto.org", 1883, 60)

con.loop_forever()