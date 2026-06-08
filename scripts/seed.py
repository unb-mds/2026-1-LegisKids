"""
seed.py — Popular banco com dados iniciais do LegisKids

Execute na raiz do projeto com o venv ativado:

    python scripts/seed.py

Requer DATABASE_URL configurada no .env (banco local Docker ou Neon).
Seguro para executar mais de uma vez — idempotente por PK.
Nunca apaga dados existentes.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.backend.app import app, db
from src.backend.models import Partido

# ── Partidos principais da Câmara dos Deputados ────────────────────────────────
# IDs conforme API: dadosabertos.camara.leg.br/api/v2/partidos
# Para verificar ou adicionar partidos:
#   GET https://dadosabertos.camara.leg.br/api/v2/partidos?itens=100
PARTIDOS_INICIAIS = [
    {"id": 12,    "sigla": "PDT",          "nome": "Partido Democrático Trabalhista"},
    {"id": 13,    "sigla": "PT",           "nome": "Partido dos Trabalhadores"},
    {"id": 15,    "sigla": "MDB",          "nome": "Movimento Democrático Brasileiro"},
    {"id": 20,    "sigla": "PODE",         "nome": "Podemos"},
    {"id": 22,    "sigla": "PL",           "nome": "Partido Liberal"},
    {"id": 37,    "sigla": "PP",           "nome": "Progressistas"},
    {"id": 40,    "sigla": "PSB",          "nome": "Partido Socialista Brasileiro"},
    {"id": 45,    "sigla": "PSDB",         "nome": "Partido da Social Democracia Brasileira"},
    {"id": 46,    "sigla": "PSOL",         "nome": "Partido Socialismo e Liberdade"},
    {"id": 55,    "sigla": "PSD",          "nome": "Partido Social Democrático"},
    {"id": 65,    "sigla": "PCdoB",        "nome": "Partido Comunista do Brasil"},
    {"id": 70,    "sigla": "Avante",       "nome": "Avante"},
    {"id": 400,   "sigla": "SD",           "nome": "Solidariedade"},
    {"id": 495,   "sigla": "PRD",          "nome": "Partido Renovação Democrática"},
    {"id": 20200, "sigla": "NOVO",         "nome": "Novo"},
    {"id": 40090, "sigla": "Republicanos", "nome": "Republicanos"},
    {"id": 40880, "sigla": "UNIÃO",        "nome": "União Brasil"},
    # Adicione mais partidos aqui seguindo o mesmo formato:
    # {"id": <id_camara>, "sigla": "<SIGLA>", "nome": "<Nome Completo>"},
]


def seed_partidos():
    print("\n── Partidos ─────────────────────────────────────────────")
    inseridos = 0
    atualizados = 0

    for dados in PARTIDOS_INICIAIS:
        existente = db.session.get(Partido, dados["id"])
        if existente is None:
            db.session.add(Partido(**dados))
            inseridos += 1
        elif existente.sigla != dados["sigla"] or existente.nome != dados["nome"]:
            existente.sigla = dados["sigla"]
            existente.nome = dados["nome"]
            atualizados += 1

    db.session.commit()
    sem_alteracao = len(PARTIDOS_INICIAIS) - inseridos - atualizados
    print(f"  {inseridos} inserido(s) | {atualizados} atualizado(s) | {sem_alteracao} sem alteração")


# ── Adicione novas funções de seed abaixo quando necessário ───────────────────
#
# def seed_<tabela>():
#     print("\n── <Tabela> ──────────────────────────────────────────────")
#     ...
#
# Siga o mesmo padrão:
# - Verificar existência por PK antes de inserir (nunca duplicar)
# - Commitar ao final da função
# - Nunca apagar registros existentes


def main():
    print("═" * 55)
    print("  LegisKids — Seed de dados iniciais")
    print(f"  Banco: {os.getenv('DATABASE_URL', '(DATABASE_URL não definida)').split('@')[-1]}")
    print("═" * 55)

    with app.app_context():
        seed_partidos()
        # seed_<outras_tabelas>()  ← adicione aqui quando necessário

    print("\n" + "═" * 55)
    print("  Seed concluído com sucesso.")
    print("═" * 55)


if __name__ == "__main__":
    main()
