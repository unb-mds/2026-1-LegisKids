## Why

O projeto carece de visibilidade sobre a participação individual dos membros ao longo do semestre. Um relatório automatizado baseado em dados reais do GitHub (commits e issues) permite que o grupo acompanhe contribuições de forma objetiva e transparente, sem depender de avaliação manual.

## What Changes

- Novo workflow `.github/workflows/performance-report.yml` disparado manualmente via `workflow_dispatch`
- Novo script `scripts/generate_performance_report.py` que extrai métricas de commits (via `git log`) e issues (via API do GitHub)
- Arquivo de configuração `.github/performance-students.json` mapeando alunos para logins GitHub e e-mails de commit
- Geração de `docs/performance/metrics.json` com dados estruturados por aluno
- Geração de `docs/performance/index.html` com gráficos estáticos usando Chart.js via CDN
- Os arquivos gerados são commitados de volta ao repositório pelo próprio workflow

## Capabilities

### New Capabilities

- `performance-report-workflow`: Workflow GitHub Actions que orquestra a coleta de métricas e geração do relatório, usando apenas `GITHUB_TOKEN` com permissões mínimas (`contents: write`, `issues: read`)
- `metrics-collector`: Script Python que consolida dados do `git log` e da API de issues do GitHub (com paginação), ignora pull requests, e produz `metrics.json` estruturado por aluno
- `performance-dashboard`: Página HTML estática (`index.html`) com gráficos por aluno (commits, issues, caracteres de issues) gerada a partir do `metrics.json`

### Modified Capabilities

## Impact

- Nenhuma arquitetura existente é alterada
- Novos arquivos adicionados em `.github/`, `scripts/` e `docs/performance/`
- Dependência de runtime: Python 3.x (disponível nos runners do GitHub Actions por padrão)
- Dependência de frontend: Chart.js via CDN (sem instalação local)
- O workflow usa apenas `GITHUB_TOKEN`; nenhum segredo adicional é necessário
