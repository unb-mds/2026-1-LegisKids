# Design — filtro-proposicoes-processadas

## Arquivos afetados

| Arquivo | Ação |
|---|---|
| `src/backend/repository/camara_repository.py` | Adicionar `get_ids_existentes` |
| `src/backend/services/camara_service.py` | Dois filtros em `run_sync` |
| `tests/test_camara_repository.py` | Novos casos de teste |

---

## 1. Nova função `get_ids_existentes` no repositório

```python
def get_ids_existentes(ids: list[int]) -> set[int]:
    """Retorna o subconjunto de IDs que já existem na tabela proposicoes."""
    if not ids:
        return set()
    rows = db.session.query(Proposicao.id).filter(Proposicao.id.in_(ids)).all()
    return {row[0] for row in rows}
```

Uma única query `SELECT id FROM proposicoes WHERE id IN (...)` — sem carregar os objetos completos. Retorna `set[int]` para lookup O(1).

---

## 2. Filtro 1 — Early-stop de paginação em `run_sync`

**Onde:** logo após `_buscar_proposicoes_api(pagina)`, antes do filtro de palavras-chave.

**Lógica:**

```python
dados_brutos = _buscar_proposicoes_api(pagina)
if not dados_brutos:
    break

ids_brutos = [d["id"] for d in dados_brutos]
ids_conhecidos = repo.get_ids_existentes(ids_brutos)

if len(ids_conhecidos) == len(ids_brutos):
    logger.info(
        "Página %d: todos os %d IDs já no banco — paginação encerrada.",
        pagina, len(ids_brutos),
    )
    break
```

**Por que usar os IDs brutos (e não só os filtrados):** a API retorna resultados ordenados por `id DESC`. Se todos os 100 IDs de uma página já estão no banco, os de IDs ainda menores (páginas seguintes) também estarão. O filtro de palavras-chave é irrelevante para esta decisão.

**Caso de borda — primeira execução:** nenhum ID existe ainda → `len(ids_conhecidos) == 0 != len(ids_brutos)` → nunca para prematuramente.

---

## 3. Filtro 2 — Skip de Gemini para IDs já conhecidos

**Onde:** após validar os DTOs, antes de montar os lotes para o Gemini.

**Lógica:**

```python
# ids_conhecidos já foi calculado no Filtro 1 para esta página
dtos_validos = [dto for dto in dtos_validos if dto["id"] not in ids_conhecidos]
```

Proposições com ID já no banco são ignoradas completamente neste run:
- Se `classificado` → não precisa de re-processamento
- Se `pendente_classificacao` → será tratada por `_retentar_pendentes` no início do próximo run (ou do run atual, que já rodou)

**Resultado:** apenas proposições genuinamente novas chegam ao Gemini.

---

## Fluxo completo após a mudança

```
run_sync()
│
├── _retentar_pendentes()          ← classifica pendentes do DB (sem re-ler API)
│
└── loop de páginas
    ├── _buscar_proposicoes_api()
    ├── get_ids_existentes(ids_brutos)
    ├── [EARLY-STOP] se todos conhecidos → break
    ├── _filtrar_por_palavras_chave()
    ├── _validar_proposicao() para cada dado
    ├── [SKIP] filtra IDs já no banco de dtos_validos
    └── _classificar_lote() → Gemini apenas para novos
```

---

## Reutilização de `ids_conhecidos`

Os dois filtros usam a **mesma chamada** a `get_ids_existentes` por página — sem query duplicada:

```python
ids_brutos = [d["id"] for d in dados_brutos]
ids_conhecidos = repo.get_ids_existentes(ids_brutos)   # 1 query por página

# Filtro 1
if len(ids_conhecidos) == len(ids_brutos):
    break

# ... keyword filter, validação ...

# Filtro 2
dtos_validos = [dto for dto in dtos_validos if dto["id"] not in ids_conhecidos]
```
