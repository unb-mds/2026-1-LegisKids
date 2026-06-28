## Why

A auditoria do backend identificou dois arquivos mortos que coexistem com o service layer atual e três problemas de código que afetam corretude e manutenibilidade:

1. **`src/backend/main.py` é código morto e perigoso**: é uma CLI interativa legada com `input()` executando no nível do módulo — qualquer `import main` trava o processo. A lógica foi completamente substituída por `CamaraService` + scheduler.

2. **`src/backend/services/camara_api.py` duplica o service**: define `URL_BASE`, `filtrar_por_palavras_chave` e `listar_proposicoes` — todas reimplementadas em `camara_service.py`. Nenhum código ativo do projeto importa `camara_api.py`.

3. **`datetime.utcnow` deprecated (Python 3.12+)**: os modelos `Proposicao`, `Usuario`, `Favorito`, `HistoricoConsulta` e `RequisicaoApi` usam `default=datetime.utcnow` — método deprecated que emite `DeprecationWarning` no Python 3.12 e será removido em versões futuras. `SyncExecution` já usa o padrão correto (`lambda: datetime.now(timezone.utc)`).

4. **`vincular_categoria` faz commit por chamada**: para uma proposição com 3 categorias, são 3 commits individuais. Com lotes de 50 proposições × 3 categorias = 150 commits por lote.

## What Changes

- **Remove `src/backend/main.py`**: arquivo legado sem uso no projeto atual.
- **Remove `src/backend/services/camara_api.py`**: duplicata do service; funções já existem em `camara_service.py`.
- **`src/backend/models.py`**: substitui `datetime.utcnow` por `lambda: datetime.now(timezone.utc)` em todos os modelos afetados.
- **`src/backend/repository/camara_repository.py`**: remove o `db.session.commit()` interno de `vincular_categoria`; o commit passa a ser responsabilidade do chamador (já feito em `upsert_proposicoes_lote`).

## Capabilities

### Removed (dead code)

- `main.py`: CLI interativa legada com filtro manual de proposições.
- `camara_api.py`: wrapper direto da API da Câmara substituído pelo service layer.

### Fixed

- `datetime-utcnow-deprecation`: todos os `default=datetime.utcnow` substituídos por `lambda: datetime.now(timezone.utc)`.
- `vincular-categoria-commit`: commit removido da função; reduz de N commits por proposição para 1 commit por lote.

## Impact

- **Backend**: remoção de 2 arquivos, edições em `models.py` e `camara_repository.py`.
- **Testes**: verificar se algum teste importa `main.py` ou `camara_api.py` e remover/adaptar.
- **Sem impacto**: rotas Flask, scheduler, Gemini integration, frontend.
