# Design — sync-camara-gemini-batch-queue

## Fluxo atual vs. fluxo proposto

### Atual (classifica por página)

```
Página 1 → filtra → 3 DTOs → Gemini(3) → persiste
Página 2 → filtra → 1 DTO  → Gemini(1) → persiste
Página 3 → filtra → 5 DTOs → Gemini(5) → persiste
...
Total: N páginas = N chamadas ao Gemini (com lotes menores que BATCH_SIZE)
```

### Proposto (fila acumulada)

```
Página 1 → filtra → 3 DTOs → fila=[3]
Página 2 → filtra → 1 DTO  → fila=[4]
Página 3 → filtra → 5 DTOs → fila=[9]
Página 4 → filtra → 2 DTOs → fila=[11] → Gemini(10) → persiste → fila=[1]
...
Fim da paginação → Gemini(fila restante) → persiste
```

Com `GEMINI_BATCH_SIZE=10`, o número de chamadas ao Gemini cai de `ceil(total_relevantes / média_por_página)` para `ceil(total_relevantes / BATCH_SIZE)`.

## Mudança em `run_sync()`

### Estrutura da fila

```python
fila_dtos: list[dict] = []  # acumula DTOs válidos e novos entre páginas
```

A variável existe fora do `while True` e persiste entre iterações.

### Loop de paginação (novo)

```python
while True:
    # ... busca, early-stop, filtra, valida, remove conhecidos (inalterados) ...

    dtos_validos = [dto for dto in dtos_validos if dto["id"] not in ids_conhecidos]
    fila_dtos.extend(dtos_validos)
    total_processados += len(filtrados)

    # Drena a fila em lotes completos
    while len(fila_dtos) >= self._batch_size:
        lote = fila_dtos[:self._batch_size]
        fila_dtos = fila_dtos[self._batch_size:]
        _classificar_e_persistir_lote(lote)  # ver abaixo

    pagina += 1

# Drena o restante da fila (lote incompleto final)
if fila_dtos:
    _classificar_e_persistir_lote(fila_dtos)
```

### Extração de `_classificar_e_persistir_lote`

Para não duplicar o bloco de classificação + persistência, o código atual (que já existe dentro do loop) é extraído para um bloco inline ou método privado:

```python
def _classificar_e_persistir_lote(self, lote: list[dict]) -> tuple[int, int, int]:
    """Classifica um lote via Gemini e persiste. Retorna (inseridos, atualizados, descartados)."""
    if cota_gemini_esgotada:
        for dto in lote:
            dto["classificacao_status"] = Proposicao.CLASSIFICACAO_PENDENTE
        pares = [(dto, None) for dto in lote]
    else:
        pares = self._classificar_lote(lote)
        if all(categorias is None for _, categorias in pares):
            # sinaliza externamente via retorno ou flag compartilhada
            ...

    para_persistir = [(dto, cat) for dto, cat in pares if cat != [RESULTADO_IRRELEVANTE]]
    descartados = len(pares) - len(para_persistir)

    if para_persistir:
        dtos_apenas = [d for d, _ in para_persistir]
        contadores = repo.upsert_proposicoes_lote(dtos_apenas)
        for dto, categorias in para_persistir:
            if categorias:
                repo.vincular_categorias_lote(dto["id"], categorias)
        return contadores["inseridos"], contadores["atualizados"], descartados

    return 0, 0, descartados
```

> **Nota de implementação**: `cota_gemini_esgotada` é uma variável de estado do `run_sync()`. O método auxiliar pode receber a flag como parâmetro e retornar se deve ser marcada como esgotada — ou pode-se manter a lógica inline dentro de `run_sync()` com uma função local (`nonlocal`), dependendo da clareza preferida.

## Invariantes preservados

| Invariante | Como é preservado |
|---|---|
| Early-stop por IDs conhecidos | Inalterado — ocorre antes de adicionar à fila |
| Proposições irrelevantes não persistidas | Inalterado — `_classificar_lote` retorna `[RESULTADO_IRRELEVANTE]` e são filtradas antes do upsert |
| `cota_gemini_esgotada` para de chamar Gemini no run | Preservado — verificado antes de cada lote drenado da fila |
| Retry de pendentes no início do run | Inalterado — `_retentar_pendentes()` roda antes do loop |
| `SyncExecution` registrada com totais corretos | Preservado — contadores acumulados da mesma forma |

## Impacto em chamadas ao Gemini

Dado `GEMINI_BATCH_SIZE=10` e uma run típica com 30 proposições relevantes espalhadas em 15 páginas (média 2/página):

| Modelo | Chamadas ao Gemini |
|---|---|
| Atual | 15 (uma por página com proposições) |
| Proposto | 3 (lotes de 10 completos) |

Redução de 80% nas chamadas — dentro do limite de 20/dia do free tier com mais margem.
