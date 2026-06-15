"""remove autores

Revision ID: 68e1ed03a63c
Revises: 45778e94407e
Create Date: 2026-06-15 13:41:30.994607

"""
from alembic import op
import sqlalchemy as sa


revision = '68e1ed03a63c'
down_revision = '45778e94407e'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Remove índice e FK e coluna autor_id de proposicoes primeiro
    with op.batch_alter_table('proposicoes', schema=None) as batch_op:
        batch_op.drop_index('idx_proposicoes_autor_id')
        batch_op.drop_constraint('proposicoes_autor_id_fkey', type_='foreignkey')
        batch_op.drop_column('autor_id')

    # 2. Remove constraint de favoritos
    with op.batch_alter_table('favoritos', schema=None) as batch_op:
        batch_op.drop_constraint('favoritos_usuario_id_proposicao_id_key', type_='unique')

    # 3. Agora sim dropa a tabela autores
    op.drop_table('autores')


def downgrade():
    with op.batch_alter_table('proposicoes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('autor_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('proposicoes_autor_id_fkey', 'autores', ['autor_id'], ['id'])
        batch_op.create_index('idx_proposicoes_autor_id', ['autor_id'], unique=False)

    with op.batch_alter_table('favoritos', schema=None) as batch_op:
        batch_op.create_unique_constraint('favoritos_usuario_id_proposicao_id_key', ['usuario_id', 'proposicao_id'])

    op.create_table('autores',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('nome', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
        sa.Column('partido', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
        sa.Column('uf', sa.VARCHAR(length=2), autoincrement=False, nullable=True),
        sa.Column('tipo', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
        sa.Column('id_externo', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('email', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
        sa.Column('url_foto', sa.VARCHAR(length=300), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint('id', name='autores_pkey'),
        sa.UniqueConstraint('email', name='uq_autores_email'),
        sa.UniqueConstraint('id_externo', name='autores_id_externo_key'),
    )