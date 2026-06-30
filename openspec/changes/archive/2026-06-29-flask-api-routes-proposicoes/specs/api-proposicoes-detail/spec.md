## ADDED Requirements

### Requirement: Detalhe completo de proposição
O sistema SHALL expor `GET /api/proposicoes/<int:id>` retornando todos os dados de uma proposição, incluindo categorias e histórico de tramitação. A resposta SHALL ter a forma `{ proposicao: {...}, tramitacoes: [...] }`.

#### Scenario: Proposição encontrada
- **WHEN** cliente faz `GET /api/proposicoes/123` e proposição 123 existe
- **THEN** sistema retorna HTTP 200 com `proposicao` contendo todos os campos e `tramitacoes` ordenadas cronologicamente

#### Scenario: Campos obrigatórios na proposição
- **WHEN** sistema retorna a proposição
- **THEN** o objeto SHALL conter: `id`, `ementa`, `sigla_tipo`, `numero`, `ano`, `data_apresentacao`, `descricao_situacao`, `status` (alias), `sigla_partido`, `partido`, `categorias`, `subtema` (nome da primeira categoria ou null), `classificacao_status`

#### Scenario: Tramitações com aliases compatíveis com frontend
- **WHEN** sistema retorna tramitações
- **THEN** cada tramitação SHALL conter: `data_hora`, `data` (alias de data_hora), `descricao_tramitacao`, `descricao` (alias), `sigla_orgao`, `orgao` (alias), `descricao_situacao`, `id_situacao`; ordenadas por `data_hora` ASC

#### Scenario: Proposição sem tramitações
- **WHEN** proposição não tem tramitações registradas
- **THEN** sistema retorna `tramitacoes: []`

#### Scenario: Proposição não encontrada
- **WHEN** cliente faz `GET /api/proposicoes/99999` e proposição não existe
- **THEN** sistema retorna HTTP 404 com `{"error": "Proposição não encontrada"}`
