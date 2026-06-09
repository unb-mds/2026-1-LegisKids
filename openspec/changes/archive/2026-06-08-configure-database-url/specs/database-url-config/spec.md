## ADDED Requirements

### Requirement: Conexão ao banco via DATABASE_URL
O sistema SHALL usar exclusivamente a variável de ambiente `DATABASE_URL` para configurar `SQLALCHEMY_DATABASE_URI`. A aplicação SHALL levantar `RuntimeError` com mensagem descritiva se `DATABASE_URL` não estiver definida no ambiente.

#### Scenario: DATABASE_URL definida corretamente
- **WHEN** a variável `DATABASE_URL` está presente no ambiente com uma connection string PostgreSQL válida
- **THEN** o SQLAlchemy usa essa URL intacta para conectar ao banco, sem modificação

#### Scenario: DATABASE_URL ausente
- **WHEN** a variável `DATABASE_URL` não está definida no ambiente
- **THEN** a aplicação levanta `RuntimeError` com mensagem indicando que `DATABASE_URL` não foi configurada

#### Scenario: DATABASE_URL com sslmode=require (Neon)
- **WHEN** a `DATABASE_URL` contém o parâmetro `?sslmode=require`
- **THEN** o parâmetro é preservado intacto e repassado ao SQLAlchemy, estabelecendo conexão SSL com o banco remoto

### Requirement: .env.example documentado e seguro
O arquivo `.env.example` SHALL conter exemplos de `DATABASE_URL` para os dois modos de uso (Docker local e Neon remoto), usando somente valores placeholder. O arquivo NÃO SHALL conter credenciais reais, hosts reais do Neon ou chaves secretas reais.

#### Scenario: Desenvolvedor clona o repositório
- **WHEN** um novo desenvolvedor clona o repositório e abre `.env.example`
- **THEN** encontra exemplos claros de `DATABASE_URL` para banco local e remoto, com instruções de como substituir os placeholders

#### Scenario: Auditoria de segurança do repositório
- **WHEN** qualquer pessoa inspeciona o histórico git do repositório
- **THEN** nenhum arquivo commitado contém host real do Neon, usuário real, senha real ou connection string real

### Requirement: .env protegido pelo .gitignore
O arquivo `.env` SHALL estar listado no `.gitignore` do repositório, impedindo que seja commitado acidentalmente.

#### Scenario: Desenvolvedor tenta commitar .env
- **WHEN** o desenvolvedor executa `git add .env` e tenta criar um commit
- **THEN** o Git ignora o arquivo e ele não é incluído no commit

### Requirement: README com seção de configuração do banco
O `README.md` SHALL conter uma seção dedicada explicando os dois modos de banco (Docker local e Neon remoto), com exemplos de `.env`, instruções para aplicar migrations e popular o banco.

#### Scenario: Novo desenvolvedor configura o ambiente
- **WHEN** um novo desenvolvedor lê o README
- **THEN** encontra instruções claras para criar o `.env` local, aplicar `flask db upgrade` e executar `python scripts/seed.py`

### Requirement: Migrations aplicadas no banco Neon
O schema do banco Neon SHALL estar atualizado com todas as migrations existentes após a execução de `flask db upgrade` com `DATABASE_URL` apontando para o Neon.

#### Scenario: Aplicação de migrations no Neon
- **WHEN** o comando `flask db upgrade` é executado com `DATABASE_URL` apontando para o banco Neon
- **THEN** todas as tabelas definidas nas migrations são criadas no banco remoto sem erros

### Requirement: Banco Neon populado com dados iniciais
O banco Neon SHALL conter os dados iniciais necessários após a execução de `python scripts/seed.py`.

#### Scenario: Execução do seed no Neon
- **WHEN** o comando `python scripts/seed.py` é executado com `DATABASE_URL` apontando para o banco Neon
- **THEN** os dados iniciais são inseridos no banco remoto e a aplicação consegue consultá-los

### Requirement: GitHub Secret DATABASE_URL configurado
O repositório SHALL ter o GitHub Secret `DATABASE_URL` configurado com a connection string real do Neon, para uso futuro em CI/CD.

#### Scenario: Workflow de CI/CD acessa o banco
- **WHEN** um workflow do GitHub Actions executa e precisa conectar ao banco de dados
- **THEN** a variável `DATABASE_URL` está disponível via GitHub Secrets, sem estar exposta em arquivos versionados
