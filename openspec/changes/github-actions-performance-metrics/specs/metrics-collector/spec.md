## ADDED Requirements

### Requirement: Leitura do arquivo de configuração de alunos
O script SHALL ler `.github/performance-students.json` para obter o mapeamento de alunos (name, github, emails) antes de processar qualquer métrica.

#### Scenario: Arquivo de configuração válido
- **WHEN** `.github/performance-students.json` existe e contém um array de objetos com `name`, `github` e `emails`
- **THEN** o script inicializa uma entrada no relatório para cada aluno configurado

#### Scenario: Arquivo de configuração ausente
- **WHEN** `.github/performance-students.json` não existe
- **THEN** o script encerra com mensagem de erro clara indicando que o arquivo de configuração é obrigatório

### Requirement: Coleta de commits via git log
O script SHALL executar `git log` com formato estruturado para extrair, de cada commit: hash, autor (nome), e-mail, data (ISO 8601) e mensagem.

#### Scenario: Commits atribuídos ao aluno correto
- **WHEN** um commit tem e-mail que consta no array `emails` de um aluno em `performance-students.json`
- **THEN** esse commit é contabilizado nas métricas desse aluno

#### Scenario: Commit com e-mail não mapeado
- **WHEN** um commit tem e-mail que não consta em nenhum aluno configurado
- **THEN** o commit é incluído na lista global `commits` do JSON mas não é atribuído a nenhum aluno

### Requirement: Coleta de issues via API do GitHub com paginação
O script SHALL consultar a API do GitHub (`/repos/{owner}/{repo}/issues?state=all&per_page=100`) percorrendo todas as páginas até não haver mais resultados.

#### Scenario: Paginação completa
- **WHEN** o repositório tem mais de 100 issues
- **THEN** o script coleta todas as issues, não apenas as primeiras 100

#### Scenario: Nenhuma issue existente
- **WHEN** o repositório não tem issues
- **THEN** o script retorna uma lista vazia de issues sem erro

### Requirement: Exclusão de pull requests na contagem de issues
O script SHALL ignorar qualquer item retornado pela API de issues que possua o campo `pull_request` preenchido.

#### Scenario: Pull request excluído da contagem
- **WHEN** a API retorna um item com o campo `pull_request` não-nulo
- **THEN** esse item não é contabilizado nas métricas de issues de nenhum aluno

### Requirement: Atribuição de issues ao aluno correto
O script SHALL atribuir uma issue ao aluno cujo campo `github` (login) coincide com o campo `user.login` da issue.

#### Scenario: Issue atribuída ao criador
- **WHEN** uma issue foi criada pelo usuário com login `estudante-x`
- **THEN** a issue é contabilizada nas métricas do aluno com `github: "estudante-x"`

### Requirement: Cálculo de métricas agregadas por aluno
O script SHALL calcular, para cada aluno: `commits_count`, `issues_count`, `issue_characters_total`, `issue_characters_average`, `commit_timeline` (commits por mês/semana), `issue_timeline` (issues por mês/semana).

#### Scenario: Média de caracteres com zero issues
- **WHEN** um aluno não criou nenhuma issue
- **THEN** `issue_characters_average` é `0` (não divisão por zero)

#### Scenario: Timeline de commits por mês
- **WHEN** um aluno tem commits em diferentes meses
- **THEN** `commit_timeline` é um objeto com chaves no formato `YYYY-MM` e valores com a contagem de commits naquele mês

### Requirement: Geração do arquivo metrics.json
O script SHALL escrever `docs/performance/metrics.json` com a estrutura definida (generated_at, repository, students, commits, issues), criando o diretório se necessário.

#### Scenario: Arquivo gerado com sucesso
- **WHEN** o script conclui sem erros
- **THEN** `docs/performance/metrics.json` existe e é JSON válido com todos os campos obrigatórios da estrutura

### Requirement: Execução sem erros em repositório vazio de métricas
O script SHALL concluir sem lançar exceção quando não houver commits, issues ou quando a timeline de um período estiver vazia.

#### Scenario: Repositório sem issues
- **WHEN** o repositório não tem nenhuma issue real (somente PRs ou nada)
- **THEN** o script gera `metrics.json` com `issues: []` e `issues_count: 0` para todos os alunos
