import os
import sys
import click
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"])

_database_url = os.getenv("DATABASE_URL")
if not _database_url:
    raise RuntimeError("DATABASE_URL não configurada no ambiente.")

app.config["SQLALCHEMY_DATABASE_URI"] = _database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

from src.backend.database import db
from src.backend import models  # noqa: F401
from src.backend.controllers.proposicoes_controller import proposicoes_bp

db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(proposicoes_bp)

# Seed de categorias e scheduler (pula em modo de testes)
if os.getenv("FLASK_ENV") != "testing":
    from src.backend.repository import camara_repository as repo
    from src.backend.schedulers.camara_scheduler import start_scheduler
    with app.app_context():
        try:
            repo.seed_categorias()
        except Exception as _seed_err:
            import logging as _log
            _log.getLogger(__name__).warning(
                "seed_categorias ignorado na inicialização (migrations pendentes?): %s", _seed_err
            )
        start_scheduler(app)


@app.cli.command("sync-camara")
def sync_camara():
    """Executa sincronização manual de proposições da Câmara dos Deputados."""
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
    app.run(debug=True)