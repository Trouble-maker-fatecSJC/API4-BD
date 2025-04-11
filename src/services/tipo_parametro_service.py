import httpx
import logging

class TipoParametroService:
    def __init__(self):
        self.api_url = "http://localhost:3000/api/tipoparametro"
        
    async def get_id_parametro(self, nome_parametro: str) -> int:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.api_url)
                if response.status_code == 200:
                    tipos_parametros = response.json()
                    for tipo in tipos_parametros:
                        if tipo["nome"].lower() == nome_parametro.lower():
                            return tipo["id_tipo_param"]
                    logging.warning(f"Tipo de parâmetro não encontrado: {nome_parametro}")
                    return None
        except Exception as e:
            logging.error(f"Erro ao buscar tipo de parâmetro: {str(e)}")
            return None