import os
import sys

import click
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

app = Flask(__name__)

_flask_env = os.getenv("FLASK_ENV", "development")

_cors_origins = [o.strip() for o in os.getenv("FRONTEND_URL", "").split(",") if o.strip()]
if _flask_env != "production":
    _cors_origins += ["http://localhost:5173", "http://127.0.0.1:5173"]
CORS(app, origins=_cors_origins)

_database_url = os.getenv("DATABASE_URL")
if not _database_url:
    raise RuntimeError("DATABASE_URL não configurada no ambiente.")

app.config["SQLALCHEMY_DATABASE_URI"] = _database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

_secret_key = os.getenv("SECRET_KEY")
if not _secret_key:
    if _flask_env == "production":
        raise RuntimeError("SECRET_KEY não configurada no ambiente de produção.")
    _secret_key = "dev-secret"
app.config["SECRET_KEY"] = _secret_key

from src.backend import models  # noqa: E402,F401
from src.backend.controllers.cron_controller import cron_bp  # noqa: E402
from src.backend.controllers.proposicoes_controller import proposicoes_bp  # noqa: E402
from src.backend.database import db  # noqa: E402

db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(proposicoes_bp)
app.register_blueprint(cron_bp)

# Seed de categorias (pula em modo de testes)
if _flask_env != "testing":
    from src.backend.repository import camara_repository as repo
    with app.app_context():
        try:
            repo.seed_categorias()
        except Exception as _seed_err:
            import logging as _log
            _log.getLogger(__name__).warning(
                "seed_categorias ignorado na inicialização (migrations pendentes?): %s", _seed_err
            )

    # Scheduler in-process: só para deploys tradicionais de longa duração
    # (Render/Railway/VM). NÃO usar no Vercel — funções serverless não mantêm
    # processo em background; lá o sync roda via Vercel Cron + /api/cron/sync.
    if os.getenv("ENABLE_SCHEDULER", "false").lower() == "true":
        from src.backend.schedulers.camara_scheduler import start_scheduler
        start_scheduler(app)


@app.cli.command("sync-camara")
def sync_camara():
    """Executa sincronização manual de proposições da Câmara dos Deputados."""
    import logging as _logging
    _logging.basicConfig(
        level=_logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    from src.backend.services.camara_service import CamaraService
    click.echo("Iniciando sincronização...")
    resumo = CamaraService().run_sync()
    click.echo(
        f"Concluído: status={resumo['status']} | "
        f"processados={resumo['total_processados']} | "
        f"inseridos={resumo['total_inseridos']} | "
        f"atualizados={resumo['total_atualizados']} | "
        f"erros={resumo['total_erros']}"
    )


@app.route("/")
def index():
    return jsonify({"status": "ok", "message": "LegisKids está no ar!"})

@app.route("/health")
def health():
    try:
        with db.engine.connect():
            pass
        return jsonify({"status": "ok", "database": "conectado"}), 200
    except Exception as exc:
        return jsonify({"status": "erro", "database": str(exc)}), 500

if __name__ == "__main__":
    app.run(debug=(_flask_env == "development"))
