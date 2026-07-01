## 1. Correção da migration

- [x] 1.1 Em `migrations/versions/ded4438e4a2c_auditoria_backend_total_descartados_e_.py`, dentro de `upgrade()`, obter um `Inspector` via `sqlalchemy.inspect(op.get_bind())` antes do bloco `batch_alter_table('proposicoes', ...)`
- [x] 1.2 Condicionar `batch_op.drop_column('categoria')` para só executar se `'categoria'` estiver entre as colunas retornadas por `inspector.get_columns('proposicoes')`
- [x] 1.3 Manter inalterados os demais `create_index` do mesmo bloco e o restante da migration (`sync_executions`, `favoritos`)
- [x] 1.4 Não alterar `downgrade()`

## 2. Validação

- [ ] 2.1 **PENDENTE — validação manual**: Rodar `flask db upgrade` (ou `alembic upgrade head`) em um banco PostgreSQL local vazio e confirmar que todas as revisões aplicam sem erro, incluindo `ded4438e4a2c`. Não executado nesta sessão: sem Postgres local/Docker/CLI Neon disponíveis no ambiente, e não foi rodada contra o Neon de produção por segurança.
- [ ] 2.2 **PENDENTE — validação manual**: Confirmar que o schema resultante tem os índices `idx_proposicoes_classificacao_status` e os demais criados nessa migration, e não tem a coluna `categoria`. Depende de 2.1.
- [ ] 2.3 **PENDENTE — validação manual**: Confirmar (via leitura do schema do Neon ou dump de referência) que o resultado do upgrade do zero bate com o estado atual do Neon. Depende de 2.1.
- [x] 2.4 Rodar a suíte de testes do backend (`pytest`) para garantir que nada relacionado a `proposicoes`/migrations quebrou — 36 passed, 6 failed (falhas pré-existentes de `google.genai` no serviço Gemini, sem relação com esta mudança)
