"""Orquestracao do pipeline ETL do Cartola FC - Pessoa 2.

Ponto de entrada principal do projeto. Executa, em sequencia:
  1. Conexao ao MongoDB
  2. Busca de dados na API do Cartola FC
  3. Processamento e gravacao dos dados (clubes, atletas e status)
"""

import logging
import sys

from api import buscar_dados_mercado
from conexao import conectar_mongodb
from processamento import processar_e_gravar_dados

# ---------------------------------------------------------------------------
# Configuracao do logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Orquestracao principal
# ---------------------------------------------------------------------------
if __name__ == "__main__":

    # 1. Conectar ao MongoDB
    print("Conectando ao MongoDB...")
    try:
        db = conectar_mongodb()
    except Exception as exc:
        logger.error("Nao foi possivel conectar ao MongoDB: %s", exc)
        sys.exit(1)

    # 2. Buscar dados na API
    print("Buscando dados na API...")
    try:
        dados_mercado = buscar_dados_mercado()
    except Exception as exc:
        logger.error("Nao foi possivel obter os dados da API: %s", exc)
        sys.exit(1)

    # 3-5. Processar e gravar clubes, atletas e status
    print("Gravando dados dos clubes...")
    print("Gravando dados dos atletas...")
    print("Gravando status do mercado...")
    try:
        processar_e_gravar_dados(db, dados_mercado)
    except Exception as exc:
        logger.error("Erro durante o processamento e gravacao dos dados: %s", exc)
        sys.exit(1)

    # 6. Finalizar
    print("Finalizado com sucesso.")
