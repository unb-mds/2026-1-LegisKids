## Why

A estrutura do banco só pode ser compreendida analisando os models, migrations ou o próprio banco — não existe referência documentada e centralizada. Isso dificulta o onboarding de novos membros, a revisão de migrations futuras e o entendimento dos relacionamentos entre entidades.

## What Changes

- Criar diretório `docs/db/` com documentação centralizada do banco
- Gerar Diagrama Entidade-Relacionamento (ERD) representando o schema real: tabelas, PKs, FKs, relacionamentos 1:N e código-fonte `.dbml` para facilitar atualizações futuras
- Criar `docs/db/schema.md` com descrição de cada tabela, colunas (tipo, nulidade, descrição), constraints, índices e decisões de design
- Atualizar `README.md` com link para `docs/db/schema.md` e referência ao ERD

## Capabilities

### New Capabilities

- `schema-banco-de-dados`: Documentação estruturada do esquema do banco — ERD, tabelas, colunas, relacionamentos, constraints e decisões de modelagem

### Modified Capabilities

(nenhuma — nenhuma regra de negócio ou requisito de nível de spec é alterado; esta mudança é puramente documental)

## Impact

- `docs/db/` (novo diretório)
- `docs/db/erd.png` (novo — exportação do ERD)
- `docs/db/erd.dbml` (novo — código-fonte do ERD para edição futura)
- `docs/db/schema.md` (novo — documentação textual completa)
- `README.md` (atualizado — link para a documentação)
- `mkdocs.yml` (atualizado — entrada no nav para `docs/db/schema.md`)
