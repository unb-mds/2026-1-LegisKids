## ADDED Requirements

### Requirement: Migrations aplicáveis do zero
A cadeia de migrations Alembic do projeto SHALL poder ser aplicada por completo (`flask db upgrade` desde um banco PostgreSQL vazio até a revisão mais recente) sem erros, independentemente de o banco ter ou não passado por schemas legados anteriores.

#### Scenario: Novo integrante roda upgrade em banco vazio
- **WHEN** um novo integrante cria um banco PostgreSQL vazio e executa `flask db upgrade`
- **THEN** todas as revisões são aplicadas em sequência até a `head` sem lançar exceção, e o schema resultante é idêntico ao do banco Neon de referência

#### Scenario: Migration remove coluna legada que pode não existir
- **WHEN** uma migration precisa remover uma coluna que só existia em schemas antigos (ex: `categoria` em `proposicoes`)
- **THEN** a migration verifica a existência da coluna antes de removê-la, e não falha caso a coluna já esteja ausente

### Requirement: Migration corrigida é no-op sobre o schema já correto
Ao rodar a migration `ded4438e4a2c` contra um banco cujo schema já não possui a coluna `categoria` (como o Neon de produção), o `drop_column` SHALL ser pulado sem alterar o schema existente.

#### Scenario: Migration roda contra banco já migrado (Neon)
- **WHEN** a migration `ded4438e4a2c` é aplicada em um banco que já não tem a coluna `categoria` em `proposicoes`
- **THEN** o passo de remoção de coluna é ignorado e nenhuma alteração de schema ocorre além do que já havia sido aplicado anteriormente
