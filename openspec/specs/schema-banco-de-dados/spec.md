# Spec: schema-banco-de-dados

## Purpose

Documentar o schema do banco de dados do LegisKids de forma completa e acessível, incluindo um Diagrama Entidade-Relacionamento versionado, documentação textual de cada tabela com colunas, constraints e relacionamentos, e integração dessa documentação ao README e ao MkDocs do projeto.

## Contexto

O LegisKids utiliza PostgreSQL com SQLAlchemy e Flask-Migrate. O schema atual conta com 7 tabelas definidas nos models. Novos integrantes e revisores de PR precisam de uma referência centralizada e visual para entender a estrutura do banco, tomar decisões de design e verificar consistência entre migrations e modelos.

## Escopo

- Diagrama Entidade-Relacionamento (ERD) disponível como imagem e como código-fonte editável
- Arquivo `docs/db/schema.md` com descrição textual completa de cada tabela
- Documentação explícita de relacionamentos com cardinalidade e justificativa
- Listagem de constraints relevantes: PKs, unique constraints, FKs com comportamento `ON DELETE`
- Integração da documentação ao `README.md` e ao `mkdocs.yml`

## Requirements

### Requirement: ERD do banco disponível e versionado
O projeto SHALL possuir um Diagrama Entidade-Relacionamento representando o schema atual do banco, disponível como imagem em `docs/db/erd.png` e como código-fonte editável em `docs/db/erd.dbml`. O ERD SHALL cobrir todas as tabelas, chaves primárias, chaves estrangeiras e relacionamentos definidos nos models SQLAlchemy.

#### Scenario: Novo integrante quer entender a estrutura do banco
- **WHEN** um novo integrante acessa `docs/db/erd.png`
- **THEN** visualiza todas as 7 tabelas do banco com seus campos principais, PKs, FKs e relacionamentos representados graficamente

#### Scenario: Integrante precisa atualizar o ERD após nova migration
- **WHEN** um integrante altera `src/backend/models.py` e cria uma nova migration
- **THEN** pode editar `docs/db/erd.dbml`, reimportar no dbdiagram.io e exportar um novo `erd.png` sem depender de ferramentas instaladas localmente

### Requirement: Documentação textual do schema em schema.md
O projeto SHALL possuir o arquivo `docs/db/schema.md` descrevendo cada tabela do banco com nome, propósito, colunas (nome, tipo, nulidade, descrição), constraints e decisões de design. O arquivo SHALL referenciar o ERD via imagem embutida.

#### Scenario: Integrante quer entender o propósito de uma tabela
- **WHEN** um integrante abre `docs/db/schema.md` e procura pela tabela `tramitacoes`
- **THEN** encontra descrição do propósito da tabela, lista de colunas com tipo e descrição, e a FK para `proposicoes`

#### Scenario: Integrante quer saber se um campo é obrigatório
- **WHEN** um integrante consulta `docs/db/schema.md` para a tabela `proposicoes`
- **THEN** encontra a coluna `partido_id` marcada como opcional com a explicação de que o partido pode ser nulo caso não seja identificado na coleta

#### Scenario: Revisor de PR quer verificar se nova migration está coerente com o schema documentado
- **WHEN** um revisor lê um PR que adiciona coluna a uma tabela
- **THEN** pode comparar a mudança com o `schema.md` e o `erd.dbml` para confirmar consistência

### Requirement: Relacionamentos documentados explicitamente
O `schema.md` SHALL descrever os relacionamentos entre tabelas indicando cardinalidade (1:N) e a razão de cada relacionamento existir.

#### Scenario: Integrante quer entender por que favoritos tem duas FKs
- **WHEN** um integrante lê a seção de relacionamentos do `schema.md`
- **THEN** encontra explicação de que `favoritos` relaciona `usuarios` e `proposicoes` com constraint unique composta, impedindo duplicatas por usuário

### Requirement: Índices e constraints documentados
O `schema.md` SHALL listar as constraints relevantes: primary keys, unique constraints e foreign keys com comportamento `ON DELETE`.

#### Scenario: Integrante quer saber o que acontece ao deletar uma proposição
- **WHEN** um integrante consulta as constraints de `tramitacoes` no `schema.md`
- **THEN** encontra a FK `proposicao_id → proposicoes.id ON DELETE CASCADE` e entende que tramitações são apagadas junto com a proposição

### Requirement: README e MkDocs apontam para a documentação do banco
O `README.md` SHALL conter referência a `docs/db/schema.md` e ao ERD. O `mkdocs.yml` SHALL incluir `docs/db/schema.md` na navegação.

#### Scenario: Integrante lê o README e quer ver o schema do banco
- **WHEN** um integrante lê o README do projeto
- **THEN** encontra link ou menção a `docs/db/schema.md` e consegue navegar até a documentação sem precisar procurar no repositório

## Critérios de Aceitação

- `docs/db/erd.png` existe e representa visualmente todas as 7 tabelas com PKs, FKs e relacionamentos
- `docs/db/erd.dbml` existe como código-fonte editável do ERD
- `docs/db/schema.md` existe e descreve cada tabela com nome, propósito, colunas (nome, tipo, nulidade, descrição) e constraints
- `docs/db/schema.md` contém seção de relacionamentos com cardinalidade e justificativas
- `docs/db/schema.md` lista constraints de FK com comportamento `ON DELETE`
- `docs/db/schema.md` embute a imagem do ERD
- `README.md` contém referência a `docs/db/schema.md`
- `mkdocs.yml` inclui `docs/db/schema.md` na navegação

## Restrições

- A documentação deve refletir o estado atual dos models SQLAlchemy — não deve antecipar tabelas futuras
- O ERD deve ser mantível sem ferramentas locais obrigatórias (uso de dbdiagram.io via DBML)
- Nenhuma credencial ou dado sensível deve aparecer nos arquivos de documentação

## Testes

- Verificação manual: `docs/db/erd.png` abre e exibe todas as tabelas do schema atual
- Verificação manual: `docs/db/erd.dbml` é válido e importável no dbdiagram.io
- Verificação manual: `docs/db/schema.md` cobre todas as tabelas presentes em `src/backend/models.py`
- Verificação manual: relacionamentos descritos em `schema.md` correspondem às FKs definidas nos models
- Verificação manual: `README.md` contém link ou menção a `docs/db/schema.md`
- Verificação manual: `mkdocs.yml` lista `docs/db/schema.md` na navegação
