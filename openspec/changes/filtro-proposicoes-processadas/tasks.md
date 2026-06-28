# Tasks — filtro-proposicoes-processadas

## T1 — Adicionar `get_ids_existentes` em `camara_repository.py`

- [x] Implementar função `get_ids_existentes(ids: list[int]) -> set[int]` que retorna subconjunto de IDs já presentes na tabela `proposicoes`
- [x] Adicionar import de `Proposicao` se necessário (já importado)

## T2 — Filtro 1: early-stop de paginação em `run_sync`

- [x] Em `camara_service.py`, logo após `_buscar_proposicoes_api(pagina)` e verificação de página vazia:
  - Extrair `ids_brutos` dos dados brutos
  - Chamar `repo.get_ids_existentes(ids_brutos)`
  - Se todos os IDs conhecidos → logar e `break`

## T3 — Filtro 2: skip de IDs já conhecidos antes do Gemini

- [x] Reutilizar `ids_conhecidos` do Filtro 1 (mesma variável, sem nova query)
- [x] Após `_validar_proposicao`, filtrar `dtos_validos` excluindo IDs presentes em `ids_conhecidos`
- [x] Logar quantos DTOs foram pulados por já existirem no banco

## T4 — Testes

- [x] `test_camara_repository.py`: `TestGetIdsExistentes` com 4 casos (IDs existentes, lista vazia, nenhum existente, todos existentes)
- [x] `test_camara_repository.py`: `test_early_stop_quando_todos_ids_conhecidos` — verifica que a API é chamada apenas 1x e o Gemini não é chamado
- [x] `test_camara_repository.py`: `test_skip_gemini_para_id_ja_no_banco` — verifica que apenas o DTO novo chega ao Gemini
- [x] Rodar `pytest tests/` — 39/39 passando
