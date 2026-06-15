"""
seed.py — Popular banco com dados iniciais do LegisKids

Execute:

    .\\.venv\\Scripts\\python.exe scripts\\seed.py

Seguro para executar múltiplas vezes.
Não cria registros duplicados.
"""

import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.backend.app import app
from src.backend.database import db
from src.backend.models import (
    Partido,
    Categoria,
    Proposicao,
)

# ------------------------------------------------------------------
# PARTIDOS
# ------------------------------------------------------------------

PARTIDOS = [
    {"id": 13,    "sigla": "PT",           "nome": "Partido dos Trabalhadores"},
    {"id": 22,    "sigla": "PL",           "nome": "Partido Liberal"},
    {"id": 15,    "sigla": "MDB",          "nome": "Movimento Democrático Brasileiro"},
    {"id": 40,    "sigla": "PSB",          "nome": "Partido Socialista Brasileiro"},
    {"id": 55,    "sigla": "PSD",          "nome": "Partido Social Democrático"},
    {"id": 37,    "sigla": "PP",           "nome": "Progressistas"},
    {"id": 12,    "sigla": "PDT",          "nome": "Partido Democrático Trabalhista"},
    {"id": 46,    "sigla": "PSOL",         "nome": "Partido Socialismo e Liberdade"},
    {"id": 40880, "sigla": "UNIÃO",        "nome": "União Brasil"},
    {"id": 40090, "sigla": "REPUBLICANOS", "nome": "Republicanos"},
]

# ------------------------------------------------------------------
# CATEGORIAS
# ------------------------------------------------------------------

CATEGORIAS = [
    {
        "nome": "Educação",
        "descricao": "Projetos relacionados à educação",
        "cor": "#3B82F6",
        "icone": "educacao",
    },
    {
        "nome": "Saúde",
        "descricao": "Projetos relacionados à saúde pública",
        "cor": "#10B981",
        "icone": "saude",
    },
    {
        "nome": "Segurança",
        "descricao": "Projetos relacionados à segurança pública",
        "cor": "#EF4444",
        "icone": "seguranca",
    },
    {
        "nome": "Meio Ambiente",
        "descricao": "Projetos relacionados ao meio ambiente",
        "cor": "#22C55E",
        "icone": "meio_ambiente",
    },
]

# ------------------------------------------------------------------
# SEED PARTIDOS
# ------------------------------------------------------------------

def seed_partidos():
    inseridos = 0

    for dados in PARTIDOS:
        existente = Partido.query.filter_by(sigla=dados["sigla"]).first()
        if existente:
            continue
        db.session.add(Partido(**dados))
        inseridos += 1

    db.session.commit()
    print(f"✓ Partidos: {inseridos} inseridos")


# ------------------------------------------------------------------
# SEED CATEGORIAS
# ------------------------------------------------------------------

def seed_categorias():
    inseridos = 0

    for categoria in CATEGORIAS:
        existente = Categoria.query.filter_by(nome=categoria["nome"]).first()
        if not existente:
            db.session.add(Categoria(**categoria))
            inseridos += 1

    db.session.commit()
    print(f"✓ Categorias: {inseridos} inseridas")


# ------------------------------------------------------------------
# SEED PROPOSIÇÕES
# ------------------------------------------------------------------

SIGLAS_PARTIDOS = ["PT", "PL", "MDB", "PSB", "PSD", "PP", "PDT", "UNIÃO", "PSOL", "REPUBLICANOS"]

TEMAS = [
    "Modernização das escolas públicas",
    "Ampliação da vacinação infantil",
    "Combate ao desmatamento",
    "Fortalecimento da segurança comunitária",
    "Educação digital nas escolas",
    "Atendimento psicológico gratuito",
    "Proteção dos recursos hídricos",
    "Monitoramento urbano inteligente",
    "Capacitação de professores",
    "Incentivo à pesquisa científica",
    "Saúde preventiva",
    "Reciclagem em escolas",
    "Combate à evasão escolar",
    "Segurança nas rodovias",
    "Proteção de áreas verdes",
    "Telemedicina",
    "Bibliotecas públicas",
    "Policiamento comunitário",
    "Energia sustentável",
    "Alfabetização tecnológica",
]

def seed_proposicoes():
    categorias = Categoria.query.all()

    if not categorias:
        print("⚠ Nenhuma categoria encontrada.")
        return

    inseridas = 0

    for indice in range(20):
        numero = 101 + indice

        existente = Proposicao.query.filter_by(
            sigla_tipo="PL",
            numero=numero,
            ano=2026,
        ).first()

        if existente:
            continue

        categoria = categorias[indice % len(categorias)]
        sigla_partido = SIGLAS_PARTIDOS[indice % len(SIGLAS_PARTIDOS)]

        proposicao = Proposicao(
            sigla_tipo="PL",
            numero=numero,
            ano=2026,
            ementa=TEMAS[indice],
            data_apresentacao=date(2026, 1, (indice % 28) + 1),
            descricao_situacao="Em tramitação",
            partido_id=None,
            sigla_partido=sigla_partido,
            categoria=categoria.nome,
            url_api=f"https://dadosabertos.camara.leg.br/api/v2/proposicoes/{101 + indice}",
        )

        proposicao.categorias.append(categoria)
        db.session.add(proposicao)
        inseridas += 1

    db.session.commit()
    print(f"✓ Proposições: {inseridas} inseridas")


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------

def main():
    print("=" * 60)
    print("LegisKids - Seed")
    print("=" * 60)

    with app.app_context():
        seed_partidos()
        seed_categorias()
        seed_proposicoes()

    print("=" * 60)
    print("Seed concluída.")
    print("=" * 60)


if __name__ == "__main__":
    main()