from fastapi import APIRouter
from controllers.estacao_controller import EstacaoController

router = APIRouter(prefix="/api/v1")
controller = EstacaoController()

# Rotas para dados da estação
router.add_api_route("/dados", controller.receber_dados, methods=["POST"])
router.add_api_route("/failed-messages", controller.get_failed_messages, methods=["GET"])