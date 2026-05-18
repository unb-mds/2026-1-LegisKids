## ADDED Requirements

### Requirement: Coleta de commits atribuídos a alunos
O coletor SHALL consolidar commits do repositório e atribuí-los a alunos por e-mails configurados em `.github/performance-students.json`.

#### Scenario: Commit com e-mail mapeado
- **WHEN** um commit possui e-mail presente na configuração de um aluno
- **THEN** o commit é contado para esse aluno e aparece nos dados detalhados de commits

#### Scenario: Commit sem e-mail mapeado
- **WHEN** um commit não corresponde a nenhum aluno configurado
- **THEN** o coletor preserva o evento em uma categoria de não atribuídos ou em dados de auditoria sem quebrar a geração

### Requirement: Coleta de issues sem pull requests
O coletor SHALL coletar issues do GitHub excluindo itens que sejam pull requests.

#### Scenario: Item de issue comum
- **WHEN** a API retorna um item sem campo `pull_request`
- **THEN** o item é tratado como issue e entra nas métricas de issues

#### Scenario: Item que é pull request
- **WHEN** a API de issues retorna um item com campo `pull_request`
- **THEN** o item não é contado nas métricas de issues

### Requirement: Coleta de pull requests
O coletor SHALL coletar pull requests do repositório com autor, estado, datas principais, URL e associação ao aluno correspondente.

#### Scenario: Pull request de aluno configurado
- **WHEN** um pull request foi criado por um login GitHub presente na configuração de alunos
- **THEN** o pull request é atribuído ao aluno correspondente

#### Scenario: Pull request mergeado
- **WHEN** um pull request possui data de merge
- **THEN** o coletor registra o PR como mergeado e preserva a data de merge para métricas temporais

### Requirement: Coleta de reviews de pull requests
O coletor SHALL coletar reviews de pull requests e atribuí-las ao autor da review quando o login estiver configurado.

#### Scenario: Review de aluno configurado
- **WHEN** uma review foi feita por login GitHub presente na configuração de alunos
- **THEN** a review é contada para esse aluno

#### Scenario: Pull request sem reviews
- **WHEN** um pull request não possui reviews
- **THEN** o coletor registra zero reviews para o PR sem falhar

### Requirement: Timelines agregadas
O coletor SHALL gerar timelines agregadas por aluno e por repositório para commits, issues e pull requests.

#### Scenario: Agregação mensal
- **WHEN** existem eventos em meses diferentes
- **THEN** o JSON contém contagens agregadas por chave `YYYY-MM`

#### Scenario: Agregação semanal
- **WHEN** existem eventos em semanas diferentes
- **THEN** o JSON contém contagens agregadas por semana ISO

### Requirement: Schema público de métricas
O coletor SHALL gerar `docs/performance/metrics.json` com dados estruturados para KPIs, gráficos e tabelas do dashboard.

#### Scenario: JSON gerado com sucesso
- **WHEN** o script de geração é executado
- **THEN** `docs/performance/metrics.json` contém `generated_at`, `repository`, `students`, `summary`, `timelines`, `commits`, `issues` e `pull_requests`

#### Scenario: Repositório sem dados
- **WHEN** não há commits, issues ou pull requests atribuíveis
- **THEN** o JSON ainda é válido e contém arrays vazios ou contadores zerados

### Requirement: Paginação da API do GitHub
O coletor SHALL buscar todas as páginas necessárias da API do GitHub para issues, pull requests e reviews.

#### Scenario: Mais de cem itens
- **WHEN** a API retorna uma página completa com 100 itens
- **THEN** o coletor consulta a próxima página até não haver mais itens

### Requirement: Dados sensíveis excluídos
O coletor SHALL não escrever tokens, credenciais ou cabeçalhos de autenticação em `metrics.json` ou `index.html`.

#### Scenario: Token de execução
- **WHEN** o script usa `GITHUB_TOKEN` para consultar a API
- **THEN** o valor do token não aparece nos arquivos gerados
