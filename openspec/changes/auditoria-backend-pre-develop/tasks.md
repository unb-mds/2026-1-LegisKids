# Tasks — auditoria-backend-pre-develop

## T1 — Remover `testa_tabelas.py`

- [x] Deletar `src/backend/migrations/testa_tabelas.py`

---

## T2 — Adicionar `total_descartados` ao modelo `SyncExecution`

- [x] Em `src/backend/models.py`, adicionar coluna `total_descartados = db.Column(db.Integer, nullable=False, default=0)` após `total_erros`
- [x] Atualizar `SyncExecution.to_dict()` para incluir `'total_descartados': self.total_descartados`

---

## T3 — Adicionar índice `classificacao_status` ao modelo `Proposicao`

- [x] Em `src/backend/models.py`, adicionar `db.Index('idx_proposicoes_classificacao_status', 'classificacao_status')` em `Proposicao.__table_args__`

---

## T4 — Criar migration com coluna + índice

- [ ] Criar `migrations/versions/<rev>_auditoria_backend.py` com:
  - `batch_op.add_column` para `total_descartados` em `sync_executions` (server_default='0')
  - `batch_op.create_index` para `idx_proposicoes_classificacao_status` em `proposicoes`
- [ ] Garantir `down_revision` apontando para `f3a1b2c4d5e6`
- [ ] Rodar `flask db upgrade` e confirmar aplicação sem erros

---

## T5 — Corrigir `cota_gemini_esgotada` em `camara_service.py`

- [x] Remover o bloco `try/except Exception` externo que envolvia `self._classificar_lote(lote)` em `run_sync` (nunca é alcançado)
- [x] Após `pares = self._classificar_lote(lote)`, adicionar:
  ```python
  if all(categorias is None for _, categorias in pares):
      cota_gemini_esgotada = True
  ```
- [x] Verificar que o bloco `if cota_gemini_esgotada` (que pula lotes subsequentes) permanece intacto

---

## T6 — Passar `total_descartados` para `atualizar_sync_execution`

- [x] Em `run_sync()`, adicionar `total_descartados=total_descartados` na chamada a `repo.atualizar_sync_execution(...)`

---

## T7 — Rodar testes e verificar

- [x] `python -m pytest tests/ -q` → 39/39 passando
- [x] Confirmar que `flask db upgrade` aplica sem erro no Neon
