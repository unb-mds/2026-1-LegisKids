## MODIFIED Requirements

### Requirement: Listagem paginada de proposições
O sistema SHALL expor `GET /api/proposicoes` retornando proposições paginadas com suporte a filtros opcionais. A resposta SHALL ter a forma `{ items: [...], total: int, pagina: int, total_paginas: int }`.

#### Scenario: Requisição sem filtros retorna primeira página
- **WHEN** cliente faz `GET /api/proposicoes`
- **THEN** sistema retorna HTTP 200 com `items` (até 10 proposições), `total` (contagem total), `pagina: 1`, `total_paginas` calculado

#### Scenario: Paginação via query params
- **WHEN** cliente faz `GET /api/proposicoes?pagina=2&por_pagina=25`
- **THEN** sistema retorna a segunda página com até 25 itens; `pagina` na resposta é 2

#### Scenario: Busca textual via parâmetro q
- **WHEN** cliente faz `GET /api/proposicoes?q=cyberbullying`
- **THEN** sistema retorna apenas proposições cuja `ementa` contém "cyberbullying" (case-insensitive, match parcial)

#### Scenario: Filtro por partido
- **WHEN** cliente faz `GET /api/proposicoes?partido=PT`
- **THEN** sistema retorna apenas proposições cuja `sigla_partido` é "PT" (case-insensitive)

#### Scenario: Filtro por subtema (categoria)
- **WHEN** cliente faz `GET /api/proposicoes?subtema=cyberbullying`
- **THEN** sistema retorna apenas proposições vinculadas à categoria "cyberbullying"

#### Scenario: Filtro por intervalo de datas
- **WHEN** cliente faz `GET /api/proposicoes?data_inicio=2024-01-01&data_fim=2024-12-31`
- **THEN** sistema retorna apenas proposições com `data_apresentacao` dentro do intervalo

#### Scenario: Filtros combinados
- **WHEN** cliente faz `GET /api/proposicoes?q=criança&partido=PT&subtema=cyberbullying`
- **THEN** sistema aplica todos os filtros conjuntamente (AND)

#### Scenario: Campos obrigatórios em cada item da lista
- **WHEN** sistema retorna items na lista
- **THEN** cada item SHALL conter: `id`, `ementa`, `data_apresentacao`, `sigla_partido`, `descricao_situacao`, `status` (alias de descricao_situacao), `subtemas` (array com o nome de todas as categorias vinculadas, `[]` se nenhuma), `categorias` (array)

#### Scenario: Resultado vazio
- **WHEN** nenhuma proposição corresponde aos filtros
- **THEN** sistema retorna HTTP 200 com `items: []` e `total: 0`

### Requirement: Erros retornam JSON
O sistema SHALL retornar erros como JSON `{"error": "mensagem"}` com status HTTP adequado, nunca HTML.

#### Scenario: Parâmetro inválido
- **WHEN** cliente envia `pagina=abc` (não numérico)
- **THEN** sistema retorna HTTP 400 com `{"error": "pagina deve ser um inteiro positivo"}`
