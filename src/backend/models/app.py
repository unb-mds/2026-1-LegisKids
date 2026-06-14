from flask import Flask
from src import db

# ── Importa todos os models para que o SQLAlchemy os registre ──────────────
from src.models import Autor, Categoria, Proposicao, Usuario, Favorito  # noqa: F401


def create_app(config=None):
    app = Flask(__name__)

    # Configurações padrão
    app.config.setdefault('SQLALCHEMY_DATABASE_URI', 'sqlite:///legislativo.db')
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    app.config.setdefault('SECRET_KEY', 'dev-secret-change-in-production')

    if config:
        app.config.update(config)

    # Inicializa extensões
    db.init_app(app)

    # Cria as tabelas se não existirem
    with app.app_context():
        db.create_all()

    # Registra blueprints (adicione aqui quando criar as rotas)
    # from src.routes.proposicoes import bp as proposicoes_bp
    # app.register_blueprint(proposicoes_bp, url_prefix='/api/proposicoes')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)