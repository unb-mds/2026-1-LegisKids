# Tasks — limpeza-backend

## T1 — Verificar dependências antes de remover

- [x] Rodar `grep -r "from.*main import\|import main" src/ tests/ --include="*.py"` — deve retornar vazio
- [x] Rodar `grep -r "camara_api" src/ tests/ --include="*.py"` — deve retornar vazio ou só `camara_api.py` em si

## T2 — Remover `src/backend/main.py`

- [x] `git rm src/backend/main.py`

## T3 — Remover `src/backend/services/camara_api.py`

- [x] `git rm src/backend/services/camara_api.py`

## T4 — Corrigir `datetime.utcnow` em `models.py`

- [x] Substituir `default=datetime.utcnow` por `default=lambda: datetime.now(timezone.utc)` em:
  - `Proposicao.data_coleta`
  - `Usuario.data_criacao`
  - `Favorito.data_favorito`
  - `HistoricoConsulta.data_consulta`
  - `RequisicaoApi.data_requisicao`
- [x] Confirmar que `timezone` já está importado no topo do arquivo (já estava: `from datetime import datetime, timezone`)

## T5 — Remover commit interno de `vincular_categoria`

- [x] Em `camara_repository.py`, remover `db.session.commit()` de `vincular_categoria`
- [x] Adicionar `vincular_categorias_lote(proposicao_id, categorias)` no repositório com commit único
- [x] Atualizar `run_sync` e `_retentar_pendentes` em `camara_service.py` para usar `vincular_categorias_lote`

## T6 — Verificar testes

- [x] Atualizar `test_camara_service.py`: reescrever `TestClassificarViaGemini` → `TestClassificarLoteViaGemini`, atualizar `TestClassificarEFiltrar` para nova API de lote
- [x] Atualizar `test_camara_repository.py`: substituir patch de `_classificar_com_rate_limit` → `_classificar_lote_via_gemini`
- [x] Rodar `pytest tests/` — 33/33 passando
