import logging
import os

from flask import Blueprint, jsonify, request

logger = logging.getLogger(__name__)

cron_bp = Blueprint("cron", __name__)


@cron_bp.route("/api/cron/sync", methods=["GET", "POST"])
def sync_camara_cron():
    """Dispara CamaraService.run_sync() sob demanda.

    GET: alvo do Vercel Cron (que só dispara requisições GET e injeta
    automaticamente `Authorization: Bearer <CRON_SECRET>` quando a env var
    CRON_SECRET está configurada no projeto Vercel).
    POST: disparo manual (ex: curl) com o mesmo header de autorização.
    """
    cron_secret = os.getenv("CRON_SECRET")
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.removeprefix("Bearer ").strip()

    if not cron_secret or token != cron_secret:
        return jsonify({"error": "Não autorizado"}), 401

    from src.backend.services.camara_service import CamaraService

    try:
        resumo = CamaraService().run_sync()
    except Exception:
        logger.exception("Erro ao executar sync da Câmara via cron")
        return jsonify({"error": "Erro ao executar sincronização"}), 500

    return jsonify(resumo), 200
