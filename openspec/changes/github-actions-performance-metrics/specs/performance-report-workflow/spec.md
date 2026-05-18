## ADDED Requirements

### Requirement: Workflow executável manualmente
O workflow SHALL ser configurado com `workflow_dispatch` como único trigger, permitindo execução manual pelo GitHub Actions sem interferir em outros workflows do projeto.

#### Scenario: Execução manual bem-sucedida
- **WHEN** um usuário com permissão de escrita clica em "Run workflow" na interface do GitHub Actions
- **THEN** o workflow inicia, executa todos os steps e conclui com status `success`

### Requirement: Checkout com histórico completo
O workflow SHALL usar `actions/checkout` com `fetch-depth: 0` para garantir que o histórico completo do git esteja disponível para análise de commits.

#### Scenario: Histórico disponível para git log
- **WHEN** o step de checkout é executado
- **THEN** o comando `git log --all` no runner retorna todos os commits do repositório, não apenas o último

### Requirement: Permissões mínimas declaradas
O workflow SHALL declarar explicitamente `contents: write` e `issues: read` no bloco `permissions`, sem conceder escopos adicionais.

#### Scenario: Workflow sem escopos extras
- **WHEN** o arquivo `.github/workflows/performance-report.yml` é inspecionado
- **THEN** o campo `permissions` contém apenas `contents: write` e `issues: read`

### Requirement: Commit automático dos artefatos gerados
O workflow SHALL commitar `docs/performance/metrics.json` e `docs/performance/index.html` de volta ao repositório após a geração, usando o `GITHUB_TOKEN`.

#### Scenario: Arquivos commitados após execução
- **WHEN** o workflow conclui o step de geração do relatório
- **THEN** um novo commit contendo `docs/performance/metrics.json` e `docs/performance/index.html` é criado no branch de execução

#### Scenario: Nenhum commit criado se arquivos não mudaram
- **WHEN** o workflow é executado e os dados gerados são idênticos ao último commit
- **THEN** o step de commit é ignorado sem erro (usando `--allow-empty` ou verificação prévia de diff)

### Requirement: Disponibilização do GITHUB_TOKEN para o script
O workflow SHALL passar o `GITHUB_TOKEN` como variável de ambiente `GITHUB_TOKEN` para o step que executa o script Python.

#### Scenario: Token disponível no script
- **WHEN** o script Python é executado pelo workflow
- **THEN** `os.environ.get("GITHUB_TOKEN")` retorna um token válido não-nulo
