## 1. Refatorar `run_sync()` para fila acumulada

- [x] 1.1 Declarar `fila_dtos: list[dict] = []` antes do `while True` em `run_sync()`
- [x] 1.2 Remover o bloco `for i in range(0, len(dtos_validos), self._batch_size)` que classifica dentro do loop de páginas
- [x] 1.3 Substituir pelo acúmulo: `fila_dtos.extend(dtos_validos)` após o filtro de IDs conhecidos
- [x] 1.4 Adicionar `while len(fila_dtos) >= self._batch_size:` para drenar lotes completos dentro do loop de páginas, reutilizando a lógica de classificação + persistência já existente
- [x] 1.5 Após o `while True`, drenar o restante da fila (`if fila_dtos:`) com o mesmo bloco de classificação + persistência

## 2. Consolidar lógica de classificação + persistência

- [x] 2.1 Extrair o bloco de "classifica lote → filtra irrelevantes → upsert → vincula categorias" para um método privado `_processar_lote(self, lote, cota_esgotada) -> tuple[int, int, int, bool]` que retorna `(inseridos, atualizados, descartados, cota_agora_esgotada)`
- [x] 2.2 Substituir as duas chamadas ao bloco (lote completo e lote final) pela chamada ao novo método
- [x] 2.3 Garantir que `total_inseridos`, `total_atualizados`, `total_descartados` e `cota_gemini_esgotada` são acumulados corretamente a partir dos retornos do método

## 3. Testes

- [x] 3.1 Testar que proposições de múltiplas páginas são acumuladas antes de chamar o Gemini: mockar `_classificar_lote` e verificar que só é chamado quando `len(fila) >= BATCH_SIZE` ou ao fim da paginação
- [x] 3.2 Testar o lote residual (proposições que não completam um lote cheio): verificar que são classificadas e persistidas após a paginação terminar
- [x] 3.3 Testar que `cota_gemini_esgotada=True` faz os lotes restantes na fila serem marcados como `pendente_classificacao` sem chamar o Gemini
- [x] 3.4 Testar que os totais (`total_inseridos`, `total_descartados`) acumulam corretamente ao longo de múltiplos drenos da fila
