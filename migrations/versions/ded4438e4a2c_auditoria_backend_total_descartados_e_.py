"""auditoria_backend_total_descartados_e_indice_status

Revision ID: ded4438e4a2c
Revises: f3a1b2c4d5e6
Create Date: 2026-06-28 19:16:42.103078

Alterações:
- sync_executions: adiciona coluna total_descartados
- proposicoes: adiciona índice em classificacao_status; cria demais índices
  que estavam no modelo mas ausentes no banco; remove coluna 'categoria' legada
- favoritos: renomeia constraint única para o nome canônico do modelo
"""
from alembic import op
import sqlalchemy as sa


revision = 'ded4438e4a2c'
down_revision = 'f3a1b2c4d5e6'
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())

    # 1. Coluna total_descartados em sync_executions
    with op.batch_alter_table('sync_executions', schema=None) as batch_op:
        batch_op.add_column(sa.Column(
            'total_descartados', sa.Integer(), nullable=False, server_default='0'
        ))

    # 2. Índices em proposicoes + remoção condicional de coluna legada 'categoria'
    proposicoes_columns = {col['name'] for col in inspector.get_columns('proposicoes')}
    with op.batch_alter_table('proposicoes', schema=None) as batch_op:
        batch_op.create_index('idx_proposicoes_classificacao_status', ['classificacao_status'], unique=False)
        # Os índices abaixo podem já existir em bancos criados pela migration babbb73a5d52;
        # o IF NOT EXISTS do PostgreSQL torna a operação idempotente via IF NOT EXISTS.
        batch_op.create_index('idx_proposicoes_ano',               ['ano'],                    unique=False, if_not_exists=True)
        batch_op.create_index('idx_proposicoes_data_apresentacao', ['data_apresentacao'],       unique=False, if_not_exists=True)
        batch_op.create_index('idx_proposicoes_descricao_situacao',['descricao_situacao'],      unique=False, if_not_exists=True)
        batch_op.create_index('idx_proposicoes_partido_id',        ['partido_id'],              unique=False, if_not_exists=True)
        batch_op.create_index('idx_proposicoes_sigla_tipo',        ['sigla_tipo'],              unique=False, if_not_exists=True)
        batch_op.create_index('idx_proposicoes_tipo_ano',          ['sigla_tipo', 'ano'],       unique=False, if_not_exists=True)
        # Remove coluna legada 'categoria' apenas se ainda existir: bancos criados
        # do zero (migration babbb73a5d52) nunca a tiveram, só bancos antigos a possuem.
        if 'categoria' in proposicoes_columns:
            batch_op.drop_column('categoria')

    # 3. Favoritos: renomeia constraint única para o nome do modelo
    with op.batch_alter_table('favoritos', schema=None) as batch_op:
        batch_op.drop_constraint('favoritos_usuario_id_proposicao_id_key', type_='unique')
        batch_op.create_index('idx_favoritos_usuario_proposicao', ['usuario_id', 'proposicao_id'], unique=False)
        batch_op.create_unique_constraint('uq_favorito_usuario_proposicao', ['usuario_id', 'proposicao_id'])


def downgrade():
    with op.batch_alter_table('favoritos', schema=None) as batch_op:
        batch_op.drop_constraint('uq_favorito_usuario_proposicao', type_='unique')
        batch_op.drop_index('idx_favoritos_usuario_proposicao')
        batch_op.create_unique_constraint('favoritos_usuario_id_proposicao_id_key', ['usuario_id', 'proposicao_id'])

    with op.batch_alter_table('proposicoes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('categoria', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
        batch_op.drop_index('idx_proposicoes_classificacao_status')
        batch_op.drop_index('idx_proposicoes_tipo_ano')
        batch_op.drop_index('idx_proposicoes_sigla_tipo')
        batch_op.drop_index('idx_proposicoes_partido_id')
        batch_op.drop_index('idx_proposicoes_descricao_situacao')
        batch_op.drop_index('idx_proposicoes_data_apresentacao')
        batch_op.drop_index('idx_proposicoes_ano')

    with op.batch_alter_table('sync_executions', schema=None) as batch_op:
        batch_op.drop_column('total_descartados')
