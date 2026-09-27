"""Conexao com o banco de dados MongoDB."""

import logging
import os
from typing import Any

from dotenv import load_dotenv
from pymongo import MongoClient


logger = logging.getLogger(__name__)


def conectar_mongodb() -> Any:
    """Cria um cliente MongoDB e retorna o banco definido em DATABASE_NAME."""
    load_dotenv()
    mongodb_uri = os.getenv("MONGODB_URI")
    database_name = os.getenv("DATABASE_NAME", "cartola_fc_db")

    if not mongodb_uri:
        raise RuntimeError("A variavel MONGODB_URI nao foi definida no arquivo .env.")

    client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5_000)
    client.admin.command("ping")
    logger.info("Conexao com o MongoDB estabelecida. Banco: %s", database_name)
    return client[database_name]