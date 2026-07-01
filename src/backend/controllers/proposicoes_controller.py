import logging

from flask import Blueprint, jsonify, request

from src.backend.repository import camara_repository as repo

logger = logging.getLogger(__name__)

proposicoes_bp = Blueprint("proposicoes", __name__)


def _serializar_proposicao(prop):
    d = prop.to_dict()
    d["status"] = prop.descricao_situacao
    cats = d.get("categorias", [])
    d["subtemas"] = [c["nome"] for c in cats]
    d["nome_autor"] = None
    return d


def _serializar_tramitacao(t):
    d = t.to_dict()
    d["data"] = d["data_hora"]
    d["descricao"] = d["descricao_tramitacao"]
    d["orgao"] = d["sigla_orgao"]
    return d


@proposicoes_bp.route("/api/proposicoes")
def listar_proposicoes():
    try:
        pagina = int(request.args.get("pagina", 1))
        por_pagina = int(request.args.get("por_pagina", 10))
        if pagina < 1 or por_pagina < 1:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "pagina e por_pagina devem ser inteiros positivos"}), 400

    por_pagina = min(por_pagina, 50)

    filtros = {
        "q": request.args.get("q") or None,
        "parlamentar": request.args.get("parlamentar") or None,
        "partido": request.args.get("partido") or None,
        "data_inicio": request.args.get("data_inicio") or None,
        "data_fim": request.args.get("data_fim") or None,
        "subtema": request.args.get("subtema") or None,
    }

    try:
        items, total = repo.listar_proposicoes_paginado(filtros, pagina, por_pagina)
    except Exception as exc:
        logger.exception("Erro ao listar proposições")
        return jsonify({"error": "Erro ao buscar proposições"}), 500

    total_paginas = (total + por_pagina - 1) // por_pagina if por_pagina else 1

    return jsonify({
        "items": [_serializar_proposicao(p) for p in items],
        "total": total,
        "pagina": pagina,
        "total_paginas": total_paginas,
    })


@proposicoes_bp.route("/api/proposicoes/<int:proposicao_id>")
def detalhe_proposicao(proposicao_id):
    try:
        prop = repo.get_proposicao_detalhe(proposicao_id)
    except Exception as exc:
        logger.exception("Erro ao buscar proposição %s", proposicao_id)
        return jsonify({"error": "Erro ao buscar proposição"}), 500

    if prop is None:
        return jsonify({"error": "Proposição não encontrada"}), 404

    tramitacoes = sorted(prop.tramitacoes.all(), key=lambda t: t.data_hora)

    return jsonify({
        "proposicao": _serializar_proposicao(prop),
        "tramitacoes": [_serializar_tramitacao(t) for t in tramitacoes],
    })


@proposicoes_bp.route("/api/estatisticas")
def estatisticas():
    try:
        dados = repo.get_estatisticas_dashboard()
    except Exception as exc:
        logger.exception("Erro ao calcular estatísticas")
        return jsonify({"error": "Erro ao calcular estatísticas"}), 500

    return jsonify({
        "resumo": {
            "total": dados["total"],
            "ativas": dados["ativas"],
            "subtemas": dados["subtemas"],
            "alertas": 0,
        },
        "ultima_atualizacao": dados["ultima_atualizacao"],
        "por_subtema": dados["por_subtema"],
        "por_status": dados["por_status"],
        "temporal": dados["temporal"],
        "temporal_por_subtema": dados["temporal_por_subtema"],
        "periodo": dados["periodo"],
    })


@proposicoes_bp.route("/api/temas")
def temas():
    try:
        categorias = repo.listar_categorias_com_total()
    except Exception as exc:
        logger.exception("Erro ao listar temas")
        return jsonify({"error": "Erro ao listar temas"}), 500

    return jsonify(categorias)


@proposicoes_bp.app_errorhandler(404)
def not_found(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Recurso não encontrado"}), 404
    return e


@proposicoes_bp.app_errorhandler(500)
def internal_error(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Erro interno do servidor"}), 500
    return e
