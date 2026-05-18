## 1. Diagnóstico

- [x] 1.1 Inspecionar `docs/performance/index.html` para confirmar onde a renderização para
- [x] 1.2 Identificar a causa no gerador `scripts/generate_performance_report.py`

## 2. Correção

- [x] 2.1 Remover `string.Template` da geração do HTML
- [x] 2.2 Substituir variáveis do HTML com placeholders sentinela que não conflitam com template literals JavaScript
- [x] 2.3 Regenerar `docs/performance/index.html` e `docs/performance/metrics.json`

## 3. Validação

- [x] 3.1 Compilar `scripts/generate_performance_report.py`
- [x] 3.2 Validar a sintaxe do JavaScript extraído do HTML com `node --check`
- [x] 3.3 Confirmar que o HTML final não contém a estrutura antiga como corpo principal
- [x] 3.4 Confirmar que o dashboard contém filtros, KPIs, gráficos e tabelas
