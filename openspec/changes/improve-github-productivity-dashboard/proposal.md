## Why

O relatório atual de produtividade mostra apenas totais agregados, o que dificulta entender evolução ao longo do tempo, distribuição de trabalho e gargalos reais do squad. Melhorar o `docs/performance/index.html` com métricas interativas torna os dados do GitHub mais úteis para acompanhamento semanal, retrospectivas e tomada de decisão do grupo.

## What Changes

- Ampliar o dashboard estático em `docs/performance/index.html` com filtros interativos por aluno, período e tipo de métrica.
- Adicionar cartões de KPIs com totais do repositório, médias por aluno e destaques de atividade recente.
- Exibir gráficos temporais de commits, issues e pull requests por semana ou mês.
- Exibir gráficos comparativos por aluno para commits, issues, PRs, reviews, tamanho de issues e atividade recente.
- Adicionar tabelas detalhadas e ordenáveis para alunos, commits, issues e pull requests.
- Atualizar a geração de `metrics.json` para incluir dados relevantes adicionais do GitHub, como pull requests, reviews, estados de issues/PRs, datas de criação/fechamento e timelines consolidadas.
- Manter o relatório como HTML estático, sem servidor e sem expor tokens ou credenciais.

## Capabilities

### New Capabilities
- `github-productivity-dashboard`: Dashboard estático e interativo para análise de produtividade do squad com filtros, gráficos, KPIs e tabelas baseados em dados do GitHub.
- `metrics-collector`: Coletor que consolida commits, issues, pull requests, reviews, estados, datas e timelines necessárias para o novo dashboard.

### Modified Capabilities

## Impact

- Arquivos afetados: `scripts/generate_performance_report.py`, `docs/performance/metrics.json` e `docs/performance/index.html`.
- O workflow existente de relatório de performance continua sendo o ponto de geração dos artefatos.
- Pode exigir permissões adicionais de leitura no workflow para pull requests, caso a API usada precise de escopo explícito além de `contents: write` e `issues: read`.
- Sem novas dependências de build; o HTML continua usando bibliotecas via CDN quando necessário.
