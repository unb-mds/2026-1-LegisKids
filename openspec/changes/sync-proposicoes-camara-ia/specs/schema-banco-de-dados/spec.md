## ADDED Requirements

### Requirement: Tabela sync_executions para rastreamento de jobs
O schema SHALL incluir a tabela `sync_executions` com as colunas: `id` (SERIAL PK), `iniciado_em` (TIMESTAMP WITH TIME ZONE NOT NULL), `finalizado_em` (TIMESTAMP WITH TIME ZONE NULL), `status` (VARCHAR(30) NOT NULL — valores: `em_andamento`, `concluido`, `concluido_parcial`, `erro_api`, `erro_interno`), `total_processados` (INTEGER NOT NULL DEFAULT 0), `total_inseridos` (INTEGER NOT NULL DEFAULT 0), `total_atualizados` (INTEGER NOT NULL DEFAULT 0), `total_erros` (INTEGER NOT NULL DEFAULT 0), `mensagem_erro` (TEXT NULL).

#### Scenario: Migration cria tabela sync_executions
- **WHEN** a migration referente a esta mudança é aplicada com `flask db upgrade`
- **THEN** a tabela `sync_executions` existe no banco com todas as colunas, tipos e constraints especificados

#### Scenario: Linha de execução em andamento tem finalizado_em nulo
- **WHEN** um job é iniciado e ainda não concluiu
- **THEN** a linha em `sync_executions` tem `finalizado_em = NULL` e `status = 'em_andamento'`

### Requirement: Coluna classificacao_status em proposicoes
A tabela `proposicoes` SHALL incluir a coluna `classificacao_status` (VARCHAR(30) NOT NULL DEFAULT `'pendente_classificacao'`) para rastrear o estado da categorização por IA. Valores aceitos: `pendente_classificacao`, `classificado`.

#### Scenario: Proposição inserida sem categorização ainda
- **WHEN** uma nova proposição é inserida pelo job de sync antes da categorização Gemini
- **THEN** `classificacao_status` é `'pendente_classificacao'` por default

#### Scenario: Proposição categorizada com sucesso
- **WHEN** o Gemini retorna uma categoria válida para a proposição
- **THEN** `classificacao_status` é atualizado para `'classificado'`

## MODIFIED Requirements

### Requirement: ERD do banco disponível e versionado
O projeto SHALL possuir um Diagrama Entidade-Relacionamento representando o schema atual do banco, disponível como imagem em `docs/db/erd.png` e como código-fonte editável em `docs/db/erd.dbml`. O ERD SHALL cobrir todas as tabelas, chaves primárias, chaves estrangeiras e relacionamentos definidos nos models SQLAlchemy, incluindo as tabelas `sync_executions` e as alterações em `proposicoes` introduzidas por esta mudança.

#### Scenario: Novo integrante quer entender a estrutura do banco
- **WHEN** um novo integrante acessa `docs/db/erd.png`
- **THEN** visualiza todas as tabelas do banco (incluindo `sync_executions`) com seus campos principais, PKs, FKs e relacionamentos representados graficamente

#### Scenario: Integrante precisa atualizar o ERD após nova migration
- **WHEN** um integrante aplica a migration desta mudança
- **THEN** pode editar `docs/db/erd.dbml` para incluir `sync_executions` e `classificacao_status`, reimportar no dbdiagram.io e exportar novo `erd.png`

### Requirement: Documentação textual do schema em schema.md
O projeto SHALL possuir o arquivo `docs/db/schema.md` descrevendo cada tabela do banco com nome, propósito, colunas (nome, tipo, nulidade, descrição), constraints e decisões de design, incluindo a tabela `sync_executions` e a coluna `classificacao_status` de `proposicoes`. O arquivo SHALL referenciar o ERD via imagem embutida.

#### Scenario: Integrante quer entender o propósito da tabela sync_executions
- **WHEN** um integrante abre `docs/db/schema.md` e procura pela tabela `sync_executions`
- **THEN** encontra descrição do propósito (rastreamento de execuções do job), lista de colunas com tipo e descrição, e valores válidos do campo `status`

#### Scenario: Integrante quer entender o campo classificacao_status
- **WHEN** um integrante consulta `docs/db/schema.md` para a tabela `proposicoes`
- **THEN** encontra a coluna `classificacao_status` com descrição dos valores `pendente_classificacao` e `classificado` e a relação com o pipeline de IA
