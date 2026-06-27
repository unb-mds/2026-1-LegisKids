"""ensure categorias e proposicao_categoria existem

Revision ID: f3a1b2c4d5e6
Revises: ca57241159f9
Create Date: 2026-06-27 00:00:00.000000

Migration segura: cria as tabelas categorias e proposicao_categoria caso
não existam ainda no banco (IF NOT EXISTS). Idempotente — pode rodar
em bancos que já possuem as tabelas sem efeito colateral.
"""
from alembic import op
import sqlalchemy as sa

revision = 'f3a1b2c4d5e6'
down_revision = 'ca57241159f9'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id      SERIAL PRIMARY KEY,
            nome    VARCHAR(100) NOT NULL UNIQUE,
            descricao TEXT,
            cor     VARCHAR(7),
            icone   VARCHAR(50),
            ativa   BOOLEAN DEFAULT TRUE
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS proposicao_categoria (
            proposicao_id INTEGER NOT NULL
                REFERENCES proposicoes(id) ON DELETE CASCADE,
            categoria_id  INTEGER NOT NULL
                REFERENCES categorias(id)  ON DELETE CASCADE,
            PRIMARY KEY (proposicao_id, categoria_id)
        )
    """)


def downgrade():
    # Não derruba em downgrade — a tabela pode conter dados e a migration
    # anterior (babbb73a5d52) já gerencia o schema base.
    pass
