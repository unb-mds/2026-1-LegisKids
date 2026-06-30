## ADDED Requirements

### Requirement: Listagem de temas (categorias) com totais
O sistema SHALL expor `GET /api/temas` retornando todas as categorias ativas com o total de proposições vinculadas a cada uma. A resposta SHALL ser um array JSON.

#### Scenario: Lista de temas com contagens
- **WHEN** cliente faz `GET /api/temas`
- **THEN** sistema retorna HTTP 200 com array de objetos, cada um contendo: `id`, `nome`, `descricao`, `cor`, `icone`, `ativa`, `total` (número de proposições vinculadas)

#### Scenario: Ordenação por total DESC
- **WHEN** sistema retorna os temas
- **THEN** lista SHALL ser ordenada por `total` decrescente (temas com mais proposições primeiro)

#### Scenario: Tema sem proposições
- **WHEN** uma categoria existe mas não tem proposições vinculadas
- **THEN** esse tema aparece na lista com `total: 0`

#### Scenario: Banco sem categorias
- **WHEN** tabela categorias está vazia
- **THEN** sistema retorna HTTP 200 com array vazio `[]`
