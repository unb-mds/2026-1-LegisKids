## 1. Preparação e compatibilidade

- [x] 1.1 Revisar `scripts/generate_performance_report.py` para identificar o schema atual de `metrics.json` e os pontos de geração do HTML
- [x] 1.2 Definir helpers de normalização para datas, semanas ISO, meses, autores e associação de eventos a alunos
- [x] 1.3 Manter compatibilidade com campos atuais de `students`, `commits_count`, `issues_count`, `commit_timeline` e `issue_timeline`

## 2. Expansão da coleta de dados

- [x] 2.1 Expandir a coleta de commits para preservar lista detalhada com hash, autor, e-mail, data, mensagem, aluno associado e URL quando possível
- [x] 2.2 Expandir a coleta de issues para incluir número, título, autor, estado, datas de criação/fechamento, URL, tamanho de texto e aluno associado
- [x] 2.3 Implementar coleta paginada de pull requests com número, título, autor, estado, datas de criação/fechamento/merge, URL e aluno associado
- [x] 2.4 Implementar coleta de reviews por pull request e atribuição por login GitHub configurado
- [x] 2.5 Gerar métricas de não atribuídos para commits, issues, PRs e reviews que não correspondam a alunos configurados
- [x] 2.6 Gerar `summary` com totais do repositório, atividade recente e contadores de itens abertos, fechados e mergeados
- [x] 2.7 Gerar `timelines` agregadas por mês e semana para commits, issues e pull requests

## 3. Dashboard interativo

- [x] 3.1 Recriar `docs/performance/index.html` com layout de dashboard responsivo, filtros e seções para KPIs, gráficos e tabelas
- [x] 3.2 Implementar filtros por aluno, período, tipo de métrica e busca textual usando JavaScript puro
- [x] 3.3 Implementar cartões de KPIs recalculados conforme filtros ativos
- [x] 3.4 Implementar gráficos comparativos por aluno para commits, issues, PRs, reviews e atividade recente
- [x] 3.5 Implementar gráficos temporais semanais e mensais alternáveis
- [x] 3.6 Implementar tabelas ordenáveis de alunos, commits, issues e pull requests com links auditáveis para o GitHub
- [x] 3.7 Implementar estados vazios para métricas sem dados sem lançar erro JavaScript

## 4. Segurança e geração

- [x] 4.1 Garantir que `GITHUB_TOKEN` e cabeçalhos `Authorization` nunca sejam escritos em `metrics.json` ou `index.html`
- [x] 4.2 Confirmar que o HTML funciona via `file://` usando dados embutidos ou carregamento compatível sem CORS
- [x] 4.3 Atualizar o workflow se a coleta de PRs/reviews exigir permissão explícita adicional de leitura

## 5. Validação

- [x] 5.1 Executar `python scripts/generate_performance_report.py` localmente e verificar que `docs/performance/metrics.json` e `docs/performance/index.html` são gerados
- [x] 5.2 Inspecionar o JSON gerado para confirmar presença de `generated_at`, `repository`, `students`, `summary`, `timelines`, `commits`, `issues` e `pull_requests`
- [x] 5.3 Abrir ou validar o HTML gerado para confirmar renderização de filtros, KPIs, gráficos e tabelas
- [x] 5.4 Verificar que pull requests não são contados como issues
- [x] 5.5 Verificar que os arquivos gerados não contêm token ou credenciais
