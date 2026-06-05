import sys
from src.backend.app import app, db

def test_connection():
    with app.app_context():
        try:
            with db.engine.connect():
                print("✅  Conexão com o PostgreSQL estabelecida com sucesso!")
                return True
        except Exception as exc:
            print(f"❌  Falha: {exc}")
            return False

if __name__ == "__main__":
    sys.exit(0 if test_connection() else 1)
