from fastapi import FastAPI
import logging
import threading
from routes.estacao_routes import router as estacao_router
from routes.external_routes import router as external_router
from routes.sync_routes import router as sync_router
from services.mqtt_service import MQTTService

# Configuração do logging
logging.basicConfig(
    filename='api_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True  # Força a configuração do logging
)

app = FastAPI(title="API Estação", version="1.0.0")

# Registra as rotas
app.include_router(estacao_router)
app.include_router(external_router)
app.include_router(sync_router)

# Inicia o cliente MQTT em uma thread separada
try:
    mqtt_service = MQTTService()
    mqtt_thread = threading.Thread(target=mqtt_service.start)
    mqtt_thread.daemon = True
    mqtt_thread.start()
    logging.info("Serviço MQTT iniciado com sucesso")
except Exception as e:
    logging.error(f"Erro ao iniciar serviço MQTT: {str(e)}")

@app.on_event("startup")
async def startup_event():
    logging.info("API iniciada com sucesso")