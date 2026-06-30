# Spec: api-temas

## Objetivo

Definir o endpoint `GET /api/temas` do backend Flask, retornando todas as categorias com o total de proposições vinculadas.

## Contexto

Consumido pelo frontend para popular filtros de subtema e exibir contagens. Implementado em `src/backend/controllers/proposicoes_controller.py`; delegado a `listar_categorias_com_total` no repositório.

## Escopo

- Retorna array JSON de categorias com campo `total` adicional
- Ordenado por `total` DESC
- Inclui categorias com 0 proposições

## Requisitos

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
