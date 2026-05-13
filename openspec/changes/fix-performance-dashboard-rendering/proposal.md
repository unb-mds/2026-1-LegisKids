## Why

O relatório de desempenho está renderizando apenas o resumo por aluno porque o HTML gerado ficou inconsistente e o JavaScript para antes de inicializar filtros, KPIs, gráficos e tabelas. A correção é necessária para restaurar o dashboard como fonte confiável de acompanhamento do squad.

## What Changes

- Corrigir a geração de `docs/performance/index.html` para produzir um HTML único e íntegro, sem mistura entre a versão antiga e a versão interativa.
- Remover o uso de substituição baseada em `$...` na montagem do HTML quando houver JavaScript com template literals.
- Adicionar validação automatizada do JavaScript extraído do HTML gerado.
- Regenerar `docs/performance/index.html` e `docs/performance/metrics.json` com a versão corrigida.

## Capabilities

### New Capabilities
- `performance-dashboard-rendering`: Garantia de que o dashboard gerado carrega todo o conteúdo interativo sem erro JavaScript inicial.

### Modified Capabilities

## Impact

- Arquivo principal afetado: `scripts/generate_performance_report.py`.
- Artefatos regenerados: `docs/performance/index.html` e `docs/performance/metrics.json`.
- Sem alteração de dependências externas ou APIs.
