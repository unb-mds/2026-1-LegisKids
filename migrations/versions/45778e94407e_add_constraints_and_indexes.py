"""add constraints and indexes

Revision ID: 45778e94407e
Revises: a09e20d36ab9
Create Date: 2026-06-15 11:29:14.672944

"""
from alembic import op
import sqlalchemy as sa


revision = '45778e94407e'
down_revision = 'a09e20d36ab9'
branch_labels = None
depends_on = None


def upgrade():
    # ── autores ──────────────────────────────────────────────────────────────
    with op.batch_alter_table('autores', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=150),
               nullable=False)
        batch_op.create_unique_constraint('uq_autores_email', ['email'])

    # ── favoritos ─────────────────────────────────────────────────────────────
    with op.batch_alter_table('favoritos', schema=None) as batch_op:
        batch_op.create_index('idx_favoritos_usuario_proposicao', ['usuario_id', 'proposicao_id'], unique=False)
        batch_op.create_unique_constraint('uq_favorito_usuario_proposicao', ['usuario_id', 'proposicao_id'])

    # ── proposicoes: url_api (3 passos fora do batch) ────────────────────────
    op.add_column('proposicoes', sa.Column('url_api', sa.String(255), nullable=True))

    op.execute("""
        UPDATE proposicoes
        SET url_api = 'https://dadosabertos.camara.leg.br/proposicoes/' || id::text
        WHERE url_api IS NULL
    """)

    op.alter_column('proposicoes', 'url_api', nullable=False)
    op.create_unique_constraint('uq_proposicoes_url_api', 'proposicoes', ['url_api'])

    # ── proposicoes: índice autor_id ──────────────────────────────────────────
    with op.batch_alter_table('proposicoes', schema=None) as batch_op:
        batch_op.create_index('idx_proposicoes_autor_id', ['autor_id'], unique=False)


def downgrade():
    # ── proposicoes ───────────────────────────────────────────────────────────
    with op.batch_alter_table('proposicoes', schema=None) as batch_op:
        batch_op.drop_index('idx_proposicoes_autor_id')

    op.drop_constraint('uq_proposicoes_url_api', 'proposicoes', type_='unique')
    op.drop_column('proposicoes', 'url_api')

    # ── favoritos ─────────────────────────────────────────────────────────────
    with op.batch_alter_table('favoritos', schema=None) as batch_op:
        batch_op.drop_constraint('uq_favorito_usuario_proposicao', type_='unique')
        batch_op.drop_index('idx_favoritos_usuario_proposicao')

    # ── autores ───────────────────────────────────────────────────────────────
    with op.batch_alter_table('autores', schema=None) as batch_op:
        batch_op.drop_constraint('uq_autores_email', type_='unique')
        batch_op.alter_column('email',
               existing_type=sa.String(length=150),
               type_=sa.VARCHAR(length=200),
               nullable=True)