## ADDED Requirements

### Requirement: HTML gerado sem mistura de versões
O gerador SHALL produzir `docs/performance/index.html` com uma única estrutura de dashboard, sem combinar marcação legada do relatório antigo com a marcação interativa atual.

#### Scenario: Página contém cabeçalho interativo atual
- **WHEN** `scripts/generate_performance_report.py` gera o HTML
- **THEN** o arquivo contém o cabeçalho do dashboard interativo e não contém a estrutura antiga de "Relatório de Desempenho" como corpo principal

### Requirement: JavaScript embutido válido
O HTML gerado SHALL conter JavaScript embutido com sintaxe válida.

#### Scenario: Validação de sintaxe
- **WHEN** o script JavaScript principal é extraído de `docs/performance/index.html`
- **THEN** `node --check` executa com código de saída zero

### Requirement: Inicialização completa do dashboard
O dashboard SHALL inicializar filtros, KPIs, gráficos e tabelas sem lançar erro JavaScript antes da renderização.

#### Scenario: Funções e elementos necessários existem
- **WHEN** o dashboard executa o script principal
- **THEN** as referências a filtros, cartões, gráficos e tabelas existem no HTML gerado

### Requirement: Template seguro para JavaScript
O gerador SHALL usar um mecanismo de substituição que não interprete template literals JavaScript como placeholders do Python.

#### Scenario: Template literal preservado
- **WHEN** o HTML é gerado
- **THEN** expressões JavaScript como `${model.commits.length}` permanecem intactas no arquivo final
