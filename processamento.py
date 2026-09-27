"""Modulo de transformacao e carga (ETL Core) - Pessoa 2.

Responsavel por processar os dados brutos retornados pela API do Cartola FC
e grava-los nas respectivas colecoes do MongoDB:
  - clubes_rodada_atual
  - atletas_rodada_atual
  - mercado_rodada_atual
"""

import logging
from datetime import datetime, timezone
from typing import Any, Dict

from pymongo import UpdateOne

logger = logging.getLogger(__name__)


def _timestamp_agora() -> str:
    """Retorna o timestamp atual no formato ISO 8601 (UTC)."""
    return datetime.now(timezone.utc).isoformat()


def _processar_clubes(db: Any, dados_mercado: Dict[str, Any]) -> None:
    """Extrai, transforma e grava os clubes no MongoDB usando upsert.

    Utiliza UpdateOne com upsert=True para inserir novos clubes ou atualizar
    os existentes sem gerar duplicatas. O _id do documento e o proprio ID do clube.
    """
    clubes_raw = dados_mercado.get("clubes", {})

    if not clubes_raw:
        logger.warning("Nenhum dado de clubes encontrado na resposta da API.")
        return

    operacoes = []
    for clube_id_str, clube_data in clubes_raw.items():
        clube_id = int(clube_id_str)

        documento = {
            "_id": clube_id,
            "nome": clube_data.get("nome", ""),
            "abreviacao": clube_data.get("abreviacao", ""),
            "escudos": clube_data.get("escudos", {}),
            "nome_fantasia": clube_data.get("nome_fantasia", clube_data.get("nome", "")),
        }

        operacoes.append(
            UpdateOne(
                filter={"_id": clube_id},
                update={"$set": documento},
                upsert=True,
            )
        )

    if operacoes:
        resultado = db.clubes_rodada_atual.bulk_write(operacoes)
        logger.info(
            "Clubes processados: %d inseridos, %d atualizados.",
            resultado.upserted_count,
            resultado.modified_count,
        )


def _processar_atletas(db: Any, dados_mercado: Dict[str, Any]) -> None:
    """Extrai, transforma e grava os atletas no MongoDB.

    Limpa a colecao antes de inserir para garantir que apenas os dados
    da ultima consulta estejam presentes. Adiciona timestamp_coleta a cada atleta.
    """
    atletas_raw = dados_mercado.get("atletas", [])

    if not atletas_raw:
        logger.warning("Nenhum dado de atletas encontrado na resposta da API.")
        return

    timestamp = _timestamp_agora()
    atletas = []
    for atleta in atletas_raw:
        atleta_doc = dict(atleta)
        atleta_doc["timestamp_coleta"] = timestamp
        atletas.append(atleta_doc)

    db.atletas_rodada_atual.delete_many({})
    logger.info("Colecao atletas_rodada_atual limpa.")

    resultado = db.atletas_rodada_atual.insert_many(atletas)
    logger.info("Atletas inseridos: %d documentos.", len(resultado.inserted_ids))


def _processar_status_mercado(db: Any, dados_mercado: Dict[str, Any]) -> None:
    """Extrai, transforma e grava o status do mercado no MongoDB.

    Limpa a colecao antes de inserir para manter apenas o status mais recente.
    Adiciona timestamp_coleta ao documento.
    """
    status_doc = {
        "rodada_atual": dados_mercado.get("rodada_atual"),
        "status_mercado": dados_mercado.get("status_mercado"),
        "aviso": dados_mercado.get("aviso", ""),
        "fechamento": dados_mercado.get("fechamento", {}),
        "timestamp_coleta": _timestamp_agora(),
    }

    db.mercado_rodada_atual.delete_many({})
    logger.info("Colecao mercado_rodada_atual limpa.")

    db.mercado_rodada_atual.insert_one(status_doc)
    logger.info("Status do mercado inserido com sucesso.")


def processar_e_gravar_dados(db: Any, dados_mercado: Dict[str, Any]) -> None:
    """Funcao principal do ETL: processa e grava clubes, atletas e status.

    Args:
        db: Objeto do banco de dados MongoDB (cartola_fc_db).
        dados_mercado: Dicionario com os dados brutos retornados pela API.
    """
    logger.info("Iniciando processamento dos dados do mercado.")

    logger.info("Gravando dados dos clubes...")
    _processar_clubes(db, dados_mercado)

    logger.info("Gravando dados dos atletas...")
    _processar_atletas(db, dados_mercado)

    logger.info("Gravando status do mercado...")
    _processar_status_mercado(db, dados_mercado)

    logger.info("Processamento concluido.")
