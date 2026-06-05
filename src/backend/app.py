import os
import sys
from flask import Flask, jsonify
from flask_migrate import Migrate
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

from src.backend.database import db
from src.backend import models  # noqa: F401

db.init_app(app)
migrate = Migrate(app, db)

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