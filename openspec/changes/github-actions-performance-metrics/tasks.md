## 1. Configuração de alunos

- [x] 1.1 Criar `.github/performance-students.json` com array de alunos do Squad08, incluindo `name`, `github` (login) e `emails` (lista de e-mails usados em commits)

## 2. Script de coleta de métricas

- [x] 2.1 Criar `scripts/generate_performance_report.py` com estrutura básica: leitura de args, carregamento de `performance-students.json`, inicialização do objeto de saída
- [x] 2.2 Implementar função de coleta de commits via `subprocess` + `git log --format="%H|%an|%ae|%aI|%s" --all`
- [x] 2.3 Implementar atribuição de commits a alunos por e-mail e preenchimento de `commit_timeline` (chave `YYYY-MM`)
- [x] 2.4 Implementar função de coleta de issues via `urllib.request` com paginação (`?page=N&per_page=100`) usando `GITHUB_TOKEN`
- [x] 2.5 Implementar filtro de pull requests (excluir items com campo `pull_request` não-nulo)
- [x] 2.6 Implementar atribuição de issues a alunos por `user.login` e cálculo de `issue_characters_total`, `issue_characters_average`, `issue_timeline`
- [x] 2.7 Implementar geração de `docs/performance/metrics.json` criando o diretório se necessário
- [x] 2.8 Implementar geração de `docs/performance/index.html` com Chart.js via CDN, tabela de resumo e gráficos de commits e issues por aluno
- [x] 2.9 Garantir que o script não lance exceção quando não houver issues, commits ou alunos sem métricas (tratar divisão por zero em `issue_characters_average`)

## 3. Workflow GitHub Actions

- [x] 3.1 Criar `.github/workflows/performance-report.yml` com trigger `workflow_dispatch`
- [x] 3.2 Declarar permissões `contents: write` e `issues: read` no workflow
- [x] 3.3 Adicionar step `actions/checkout` com `fetch-depth: 0`
- [x] 3.4 Adicionar step `Set up Python` usando `actions/setup-python@v5` com Python 3.x
- [x] 3.5 Adicionar step para executar `python scripts/generate_performance_report.py` com `GITHUB_TOKEN` como variável de ambiente
- [x] 3.6 Adicionar step de commit e push dos artefatos (`docs/performance/metrics.json` e `docs/performance/index.html`) usando `git config`, `git add`, `git diff --cached --quiet || git commit`, `git push`

## 4. Validação

- [ ] 4.1 Executar o workflow manualmente via GitHub Actions e verificar que `docs/performance/metrics.json` é gerado com dados reais
- [ ] 4.2 Verificar que `docs/performance/index.html` abre no navegador e exibe gráficos com dados dos alunos
- [x] 4.3 Verificar que pull requests não aparecem nas métricas de issues
- [x] 4.4 Verificar que o `GITHUB_TOKEN` não aparece no HTML ou JSON gerados
