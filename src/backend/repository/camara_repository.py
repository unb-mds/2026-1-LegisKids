import logging
from datetime import datetime, timezone

from sqlalchemy import func
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


# ── Leitura para API pública ──────────────────────────────────────────────────

_MESES_PT = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


def listar_proposicoes_paginado(
    filtros: dict,
    pagina: int = 1,
    por_pagina: int = 10,
) -> tuple[list[Proposicao], int]:
    """Lista proposições com filtros opcionais e paginação.

    filtros aceita: q, parlamentar (ignorado — campo não existe no schema),
    partido, data_inicio, data_fim, subtema.
    Retorna (items, total).
    """
    query = db.session.query(Proposicao)

    q = filtros.get("q")
    if q:
        query = query.filter(Proposicao.ementa.ilike(f"%{q}%"))

    partido = filtros.get("partido")
    if partido:
        query = query.filter(Proposicao.sigla_partido.ilike(f"%{partido}%"))

    data_inicio = filtros.get("data_inicio")
    if data_inicio:
        query = query.filter(Proposicao.data_apresentacao >= data_inicio)

    data_fim = filtros.get("data_fim")
    if data_fim:
        query = query.filter(Proposicao.data_apresentacao <= data_fim)

    subtema = filtros.get("subtema")
    if subtema:
        query = query.filter(
            Proposicao.categorias.any(Categoria.nome.ilike(f"%{subtema}%"))
        )

    total = query.count()
    offset = (pagina - 1) * por_pagina
    items = (
        query
        .order_by(Proposicao.data_apresentacao.desc())
        .offset(offset)
        .limit(por_pagina)
        .all()
    )
    return items, total


def get_proposicao_detalhe(proposicao_id: int) -> Proposicao | None:
    """Retorna proposição por PK ou None. Tramitações e categorias via relacionamento."""
    return db.session.get(Proposicao, proposicao_id)


def get_estatisticas_dashboard() -> dict:
    """Retorna métricas agregadas para o dashboard."""
    total = db.session.query(func.count(Proposicao.id)).scalar() or 0

    ativas = (
        db.session.query(func.count(Proposicao.id))
        .filter(Proposicao.descricao_situacao == "Em tramitação")
        .scalar() or 0
    )

    subtemas = (
        db.session.query(
            func.count(func.distinct(proposicao_categoria.c.categoria_id))
        ).scalar() or 0
    )

    por_subtema_rows = (
        db.session.query(
            Categoria.nome,
            func.count(proposicao_categoria.c.proposicao_id).label("total"),
        )
        .outerjoin(proposicao_categoria, proposicao_categoria.c.categoria_id == Categoria.id)
        .group_by(Categoria.id, Categoria.nome)
        .having(func.count(proposicao_categoria.c.proposicao_id) > 0)
        .order_by(func.count(proposicao_categoria.c.proposicao_id).desc())
        .all()
    )
    por_subtema = {
        "labels": [r.nome for r in por_subtema_rows],
        "values": [r.total for r in por_subtema_rows],
    }

    por_status_rows = (
        db.session.query(Proposicao.descricao_situacao, func.count(Proposicao.id).label("total"))
        .group_by(Proposicao.descricao_situacao)
        .order_by(func.count(Proposicao.id).desc())
        .all()
    )
    por_status = {
        "labels": [r.descricao_situacao for r in por_status_rows],
        "values": [r.total for r in por_status_rows],
    }

    _ano = func.extract("year", Proposicao.data_apresentacao)
    _mes = func.extract("month", Proposicao.data_apresentacao)
    temporal_rows = (
        db.session.query(
            _ano.label("ano"),
            _mes.label("mes"),
            func.count(Proposicao.id).label("contagem"),
        )
        .group_by(_ano, _mes)
        .order_by(_ano, _mes)
        .all()
    )
    temporal = {
        "labels": [
            f"{_MESES_PT[int(r.mes) - 1]}/{int(r.ano)}" for r in temporal_rows
        ],
        "values": [r.contagem for r in temporal_rows],
    }

    ultimo_sync = (
        db.session.query(SyncExecution.finalizado_em)
        .filter(
            SyncExecution.status.in_([
                SyncExecution.STATUS_CONCLUIDO,
                SyncExecution.STATUS_CONCLUIDO_PARC,
            ])
        )
        .order_by(SyncExecution.finalizado_em.desc())
        .first()
    )
    ultima_atualizacao = (
        ultimo_sync.finalizado_em.isoformat()
        if ultimo_sync and ultimo_sync.finalizado_em
        else None
    )

    return {
        "total": total,
        "ativas": ativas,
        "subtemas": subtemas,
        "por_subtema": por_subtema,
        "por_status": por_status,
        "temporal": temporal,
        "ultima_atualizacao": ultima_atualizacao,
    }


def listar_categorias_com_total() -> list[dict]:
    """Lista todas as categorias com total de proposições vinculadas, ordenado por total DESC."""
    rows = (
        db.session.query(
            Categoria,
            func.count(proposicao_categoria.c.proposicao_id).label("total"),
        )
        .outerjoin(proposicao_categoria, proposicao_categoria.c.categoria_id == Categoria.id)
        .group_by(Categoria.id)
        .order_by(func.count(proposicao_categoria.c.proposicao_id).desc())
        .all()
    )
    return [{**cat.to_dict(), "total": total} for cat, total in rows]
