import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.data_processor_service import DataProcessorService
import asyncio
import time
import random

async def test_processor():
    processor = DataProcessorService()
    
    # Busca tipos de parâmetros disponíveis
    print("\nBuscando tipos de parâmetros...")
    param_types = await processor.get_parameter_types()
    print(f"Tipos de parâmetros encontrados: {param_types}")
    
    # Dados de teste
    test_data = {
        "estacao": {
            "uid": "bff1ec38-ed83-4f22-8bd6-5e8f4643cd24"
        },
        "parametros": [
            {
                "nome": "Chuva",
                "valor": round(random.uniform(0, 100), 2)
            },
            {
                "nome": "Direcao Vento",
                "valor": round(random.uniform(0, 360), 2)
            }
        ],
        "unix_time": int(time.time())
    }
    
    print("\nIniciando teste de processamento...")
    print(f"Dados de teste: {test_data}")
    
    # Processa e envia os dados
    result = await processor.process_and_send_data(test_data)
    
    print(f"\nResultado do processamento: {'Sucesso' if result else 'Falha'}")

if __name__ == "__main__":
    asyncio.run(test_processor())