from fastapi import FastAPI
import logging
import threading
from routes.estacao_routes import router
from services.mqtt_service import MQTTService

# Configuração do logging
logging.basicConfig(
    filename='api_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI(title="API Estação", version="1.0.0")

# Registra as rotas
app.include_router(router)

# Inicia o cliente MQTT em uma thread separada
mqtt_service = MQTTService()
mqtt_thread = threading.Thread(target=mqtt_service.start)
mqtt_thread.daemon = True
mqtt_thread.start()