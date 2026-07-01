## Why

A migration `ded4438e4a2c` remove incondicionalmente a coluna legada `categoria` da tabela `proposicoes` via `batch_op.drop_column('categoria')`. Essa coluna nunca existe em um banco criado do zero (a migration inicial `babbb73a5d52` já define `proposicoes` sem ela), então `flask db upgrade` falha com `ProgrammingError: column "categoria" does not exist` em qualquer instalação limpa — interrompendo a cadeia de migrations antes de aplicar os índices em `classificacao_status` e o ajuste de constraint em `favoritos`, que estão na mesma migration. Isso bloqueia novos integrantes e qualquer ambiente provisionado do zero.

## What Changes

- Tornar `batch_op.drop_column('categoria')` condicional em `migrations/versions/ded4438e4a2c_auditoria_backend_total_descartados_e_.py`, verificando via `sqlalchemy.inspect` (Inspector) se a coluna `categoria` existe na tabela `proposicoes` antes de removê-la.
- Nenhuma outra alteração de schema, índice ou constraint nessa migration é modificada.
- O banco Neon de referência (que já não possui a coluna `categoria`) não sofre nenhuma alteração ao rodar a migration corrigida — o `drop_column` simplesmente é pulado.

## Capabilities

### New Capabilities
- `db-migrations-fresh-install`: garante que a cadeia de migrations Alembic do projeto pode ser aplicada do zero (`flask db upgrade` em banco vazio) sem falhar, mesmo quando uma migration remove uma coluna legada que só existia em bancos antigos.

### Modified Capabilities
(nenhuma — não há spec existente cobrindo migrations)

## Impact

- Arquivo afetado: `migrations/versions/ded4438e4a2c_auditoria_backend_total_descartados_e_.py`
- Nenhum outro código, endpoint ou model é alterado
- Bancos existentes (Neon) continuam íntegros; apenas instalações novas passam a completar o `upgrade` com sucesso
