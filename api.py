"""Acesso aos dados do mercado do Cartola FC."""

import logging
from typing import Any, Dict

import requests


API_MERCADO_URL = "https://api.cartola.globo.com/atletas/mercado"
REQUEST_TIMEOUT_SECONDS = 30

logger = logging.getLogger(__name__)


def buscar_dados_mercado() -> Dict[str, Any]:
    """Busca e retorna os dados do mercado em formato Python."""
    try:
        response = requests.get(API_MERCADO_URL, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        dados = response.json()
        logger.info("Dados do mercado obtidos com sucesso.")
        return dados
    except requests.RequestException:
        logger.exception("Falha ao consultar a API do mercado do Cartola FC.")
        raise
    except ValueError:
        logger.exception("A API retornou uma resposta que nao e JSON valido.")
        raise