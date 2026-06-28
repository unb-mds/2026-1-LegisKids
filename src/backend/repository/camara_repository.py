import logging
from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import insert as pg_insert

from src.backend.database import db
from src.backend.models import Categoria, Proposicao, SyncExecution, proposicao_categoria

logger = logging.getLogger(__name__)

# ── Seed data ────────────────────────────────────────────────────────────────
SEED_CATEGORIAS = [
    {
        "nome": "cyberbullying",
        "descricao": "Proposições sobre assédio, intimidação e perseguição online envolvendo crianças e adolescentes.",
        "cor": "#EF4444",
        "icone": "shield-alert",
    },
    {
        "nome": "exploração sexual infantil online",
        "descricao": "Proposições sobre abuso, exploração sexual e pornografia infantil na internet.",
        "cor": "#DC2626",
        "icone": "alert-triangle",
    },
    {
        "nome": "proteção de dados de menores",
        "descricao": "Proposições sobre coleta, uso e proteção de dados pessoais de crianças e adolescentes.",
        "cor": "#3B82F6",
        "icone": "lock",
    },
    {
        "nome": "segurança digital infantil",
        "descricao": "Proposições sobre uso seguro da internet e ferramentas de proteção para menores.",
        "cor": "#8B5CF6",
        "icone": "shield",
    },
    {
        "nome": "regulação de plataformas digitais",
        "descricao": "Proposições sobre obrigações e responsabilidades de plataformas digitais em relação a menores.",
        "cor": "#F59E0B",
        "icone": "globe",
    },
    {
        "nome": "conteúdos nocivos para menores",
        "descricao": "Proposições sobre conteúdos impróprios, violentos ou prejudiciais a crianças e adolescentes online.",
        "cor": "#EC4899",
        "icone": "eye-off",
    },
    {
        "nome": "crimes virtuais contra crianças",
        "descricao": "Proposições sobre crimes digitais praticados contra crianças e adolescentes.",
        "cor": "#6366F1",
        "icone": "gavel",
    },
    {
        "nome": "privacidade de menores",
        "descricao": "Proposições sobre direito à privacidade e imagem de crianças e adolescentes no ambiente digital.",
        "cor": "#10B981",
        "icone": "user-shield",
    },
]

# Cache em memória nome→id para evitar N queries de lookup por run
_cache_categorias: dict[str, int] = {}


def _get_categoria_id(nome: str) -> int | None:
    if nome not in _cache_categorias:
        cat_id = db.session.query(Categoria.id).filter_by(nome=nome).scalar()
        if cat_id is not None:
            _cache_categorias[nome] = cat_id
    return _cache_categorias.get(nome)


# ── Seed ─────────────────────────────────────────────────────────────────────

def seed_categorias() -> None:
    """Insere as categorias fixas no banco se ainda não existirem (idempotente)."""
    stmt = (
        pg_insert(Categoria.__table__)
        .values(
            [
                {
                    "nome": c["nome"],
                    "descricao": c["descricao"],
                    "cor": c["cor"],
                    "icone": c["icone"],
                    "ativa": True,
                }
                for c in SEED_CATEGORIAS
            ]
        )
        .on_conflict_do_nothing(index_elements=["nome"])
    )
    db.session.execute(stmt)
    db.session.commit()
    logger.info("seed_categorias: %d categorias verificadas/inseridas.", len(SEED_CATEGORIAS))


# ── Vinculação proposicao → categoria ────────────────────────────────────────

def vincular_categoria(proposicao_id: int, categoria_nome: str) -> None:
    """Vincula proposição a uma categoria via junction table (sem commit — use vincular_categorias_lote)."""
    categoria_id = _get_categoria_id(categoria_nome)
    if categoria_id is None:
        logger.warning("vincular_categoria: categoria '%s' não encontrada no banco.", categoria_nome)
        return
    stmt = (
        pg_insert(proposicao_categoria)
        .values(proposicao_id=proposicao_id, categoria_id=categoria_id)
        .on_conflict_do_nothing()
    )
    db.session.execute(stmt)


def vincular_categorias_lote(proposicao_id: int, categoria_nomes: list[str]) -> None:
    """Vincula proposição a múltiplas categorias em um único commit."""
    for nome in categoria_nomes:
        vincular_categoria(proposicao_id, nome)
    db.session.commit()


def get_ids_existentes(ids: list[int]) -> set[int]:
    """Retorna o subconjunto de IDs que já existem na tabela proposicoes."""
    if not ids:
        return set()
    rows = db.session.query(Proposicao.id).filter(Proposicao.id.in_(ids)).all()
    return {row[0] for row in rows}


def get_proposicoes_pendentes(limite: int = 50) -> list[Proposicao]:
    """Proposições com classificação pendente, ordenadas por data_coleta ASC (mais antigas primeiro)."""
    return (
        db.session.query(Proposicao)
        .filter_by(classificacao_status=Proposicao.CLASSIFICACAO_PENDENTE)
        .order_by(Proposicao.data_coleta.asc())
        .limit(limite)
        .all()
    )


def atualizar_classificacao_status(proposicao_id: int, status: str) -> None:
    db.session.query(Proposicao).filter_by(id=proposicao_id).update(
        {"classificacao_status": status}
    )
    db.session.commit()


def deletar_proposicao(proposicao_id: int) -> None:
    """Remove proposição e seus vínculos em cascata (ON DELETE CASCADE nas FKs)."""
    prop = db.session.get(Proposicao, proposicao_id)
    if prop:
        db.session.delete(prop)
        db.session.commit()
        logger.info("Proposição %d removida (irrelevante para o tema).", proposicao_id)


# ── Proposições ──────────────────────────────────────────────────────────────

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
                    set_={col: dto[col] for col in dto if col != "id"},
                )
            )
            db.session.execute(stmt)

    db.session.commit()

    inseridos = sum(1 for d in dtos if d["id"] not in existing_ids)
    atualizados = sum(1 for d in dtos if d["id"] in existing_ids)
    return {"inseridos": inseridos, "atualizados": atualizados}


# ── SyncExecution ─────────────────────────────────────────────────────────────

def criar_sync_execution() -> SyncExecution:
    execucao = SyncExecution(
        iniciado_em=datetime.now(timezone.utc),
        status=SyncExecution.STATUS_EM_ANDAMENTO,
    )
    db.session.add(execucao)
    db.session.commit()
    logger.info("SyncExecution %d iniciada.", execucao.id)
    return execucao


def atualizar_sync_execution(execucao_id: int, **campos) -> None:
    db.session.query(SyncExecution).filter_by(id=execucao_id).update(campos)
    db.session.commit()


def get_ultimas_execucoes(limite: int = 10) -> list[SyncExecution]:
    return (
        db.session.query(SyncExecution)
        .order_by(SyncExecution.iniciado_em.desc())
        .limit(limite)
        .all()
    )
