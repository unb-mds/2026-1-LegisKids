import logging
from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import insert as pg_insert

from src.backend.database import db
from src.backend.models import Proposicao, SyncExecution

logger = logging.getLogger(__name__)


def upsert_proposicoes_lote(dtos: list[dict]) -> dict:
    """Upsert transacional de um lote de proposições.

    Retorna contadores: {'inseridos': int, 'atualizados': int}.
    Garante idempotência via INSERT ... ON CONFLICT (id) DO UPDATE.
    """
    if not dtos:
        return {"inseridos": 0, "atualizados": 0}

    ids = [d["id"] for d in dtos]
    existing_ids = {
        row[0]
        for row in db.session.query(Proposicao.id).filter(Proposicao.id.in_(ids)).all()
    }

    with db.session.begin_nested():
        for dto in dtos:
            stmt = (
                pg_insert(Proposicao.__table__)
                .values(**dto)
                .on_conflict_do_update(
                    index_elements=["id"],
                    set_={
                        col: dto[col]
                        for col in dto
                        if col != "id"
                    },
                )
            )
            db.session.execute(stmt)

    db.session.commit()

    inseridos = sum(1 for d in dtos if d["id"] not in existing_ids)
    atualizados = sum(1 for d in dtos if d["id"] in existing_ids)
    return {"inseridos": inseridos, "atualizados": atualizados}


def criar_sync_execution() -> SyncExecution:
    """Insere uma linha em sync_executions com status 'em_andamento'."""
    execucao = SyncExecution(
        iniciado_em=datetime.now(timezone.utc),
        status=SyncExecution.STATUS_EM_ANDAMENTO,
    )
    db.session.add(execucao)
    db.session.commit()
    logger.info("SyncExecution %d iniciada.", execucao.id)
    return execucao


def atualizar_sync_execution(execucao_id: int, **campos) -> None:
    """Atualiza campos de uma SyncExecution existente."""
    db.session.query(SyncExecution).filter_by(id=execucao_id).update(campos)
    db.session.commit()


def get_ultimas_execucoes(limite: int = 10) -> list[SyncExecution]:
    """Retorna as N execuções mais recentes, ordenadas por iniciado_em DESC."""
    return (
        db.session.query(SyncExecution)
        .order_by(SyncExecution.iniciado_em.desc())
        .limit(limite)
        .all()
    )
