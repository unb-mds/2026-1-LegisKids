# Spec: api-estatisticas

## Objetivo

Definir o endpoint `GET /api/estatisticas` do backend Flask, fornecendo métricas agregadas para o DashboardView.

## Contexto

O frontend (DashboardView) chama esta rota ao montar e distribui os dados para os cards de resumo e três gráficos Chart.js: barras (por_subtema), pizza (por_status) e linha (temporal). Implementado em `src/backend/controllers/proposicoes_controller.py`; delegado a `get_estatisticas_dashboard` no repositório.

## Escopo

- Resposta obrigatória: `resumo`, `ultima_atualizacao`, `por_subtema`, `por_status`, `temporal`
- `alertas` fixo em 0 (feature de R2)
- `temporal` agrupado por mês/ano com labels "MMM/YYYY" em português
- `ultima_atualizacao` derivado de `sync_executions` com status de sucesso

## Requisitos

### Requirement: Estatísticas para o dashboard
O sistema SHALL expor `GET /api/estatisticas` retornando métricas agregadas para alimentar os widgets e gráficos do DashboardView. A resposta SHALL conter `resumo`, `ultima_atualizacao`, `por_subtema`, `por_status` e `temporal`.

#### Scenario: Estrutura completa da resposta
- **WHEN** cliente faz `GET /api/estatisticas`
- **THEN** sistema retorna HTTP 200 com objeto contendo todas as 5 chaves: `resumo`, `ultima_atualizacao`, `por_subtema`, `por_status`, `temporal`

#### Scenario: Resumo com contagens gerais
- **WHEN** sistema processa a rota
- **THEN** `resumo` SHALL conter: `total` (COUNT todas as proposições), `ativas` (COUNT onde descricao_situacao = 'Em tramitação'), `subtemas` (COUNT categorias distintas vinculadas a pelo menos uma proposição), `alertas` (retornar 0 — feature de R2)

#### Scenario: Data do último sync bem-sucedido
- **WHEN** existem sync_executions com status 'concluido' ou 'concluido_parcial'
- **THEN** `ultima_atualizacao` SHALL ser o `finalizado_em` do sync mais recente bem-sucedido (ISO 8601)

#### Scenario: Sem syncs bem-sucedidos
- **WHEN** não há sync_executions com status de sucesso
- **THEN** `ultima_atualizacao` SHALL ser null

#### Scenario: Distribuição por subtema para gráfico de barras
- **WHEN** sistema processa por_subtema
- **THEN** SHALL retornar `{ labels: [array de nomes de categorias], values: [array de contagens] }` com pares posicionalmente alinhados, ordenado por contagem DESC

#### Scenario: Distribuição por status para gráfico de pizza
- **WHEN** sistema processa por_status
- **THEN** SHALL retornar `{ labels: [array de descricao_situacao distintas], values: [array de contagens] }` com todas as proposições cobertos

#### Scenario: Evolução temporal para gráfico de linha
- **WHEN** sistema processa temporal
- **THEN** SHALL retornar `{ labels: [array de strings "MMM/YYYY" ex: "Jan/2024"], values: [array de contagens] }` agrupado por mês de data_apresentacao, ordenado ASC

#### Scenario: Banco sem dados
- **WHEN** tabela proposicoes está vazia
- **THEN** `resumo.total` é 0; `por_subtema`, `por_status`, `temporal` retornam `{ labels: [], values: [] }`
