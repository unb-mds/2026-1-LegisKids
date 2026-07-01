## Why

O dashboard já exibe "Última atualização: <data>", mas isso só informa quando o job rodou pela última vez — não diz nada sobre a cobertura temporal dos dados. Um usuário não tem como saber, olhando o dashboard, se a base cobre só o último mês ou desde 2022. Isso é relevante porque o backend usa `CAMARA_DATA_INICIO` para limitar a coleta e roda com cota diária do Gemini (`GEMINI_RATE_LIMIT_RPD`), então o período efetivamente coberto pelas proposições salvas pode mudar de execução para execução e vale a pena deixar isso visível.

## What Changes

- **Backend**: `GET /api/estatisticas` passa a retornar um campo `periodo` com `data_inicio` e `data_fim`, calculados como o mínimo e o máximo de `Proposicao.data_apresentacao` entre as proposições salvas no banco.
- **Frontend**: `DashboardView.vue` ganha uma segunda "flag" no cabeçalho, ao lado de "Última atualização", no formato "Proposições salvas de DD/MM/AAAA até DD/MM/AAAA", reaproveitando o estilo visual (`.last-update`) já usado na flag existente.
- Caso não haja nenhuma proposição salva (banco vazio), a flag não é exibida.

## Capabilities

### Modified Capabilities

- `estatisticas-dashboard`: o endpoint `/api/estatisticas` passa a incluir o intervalo de datas (`periodo.data_inicio` / `periodo.data_fim`) cobertas pelas proposições salvas.
- `dashboard-principal` (Vue): novo indicador visual de período de dados no cabeçalho do dashboard.

## Impact

- **Backend**: `camara_repository.py` (nova consulta MIN/MAX em `get_estatisticas_dashboard`), `proposicoes_controller.py` (inclui `periodo` na resposta de `/api/estatisticas`).
- **Frontend**: `src/frontend/src/views/DashboardView.vue` (novo `<span>` de flag + lógica de formatação de data).
- **Sem impacto**: schema do banco, autenticação, scheduler, outras rotas.
