## 1. Backend — cálculo e exposição do período

- [x] 1.1 Em `get_estatisticas_dashboard` (`src/backend/repository/camara_repository.py`), adicionar consulta `func.min(Proposicao.data_apresentacao)` / `func.max(Proposicao.data_apresentacao)` e incluir no dict retornado como `periodo: {"data_inicio": ..., "data_fim": ...}` (ou `None` se banco vazio)
- [x] 1.2 Em `proposicoes_controller.py`, incluir `dados["periodo"]` na resposta JSON de `/api/estatisticas`

## 2. Frontend — flag no dashboard

- [x] 2.1 Em `DashboardView.vue`, adicionar `const periodoTexto = ref('')` e preencher no `onMounted` a partir de `data.periodo`, formatando `data_inicio`/`data_fim` como `DD/MM/AAAA` (formatação manual via split, evitando shift de timezone do `Date`)
- [x] 2.2 Adicionar novo `<span v-if="periodoTexto" class="last-update">Proposições salvas de {{ periodoTexto }}</span>` ao lado da flag "Última atualização" no `dashboard-header`, agrupados em `.header-flags`
- [x] 2.3 Garantir que a ausência de `periodo` (banco vazio) não quebra a renderização (flag simplesmente não aparece)

## 3. Validação

- [x] 3.1 Testar manualmente com o backend rodando (`flask run`) e dados reais no Neon — conferir se as datas exibidas batem com `MIN`/`MAX` de `data_apresentacao` no banco. Confirmado: `GET /api/estatisticas` retornou `periodo: {"data_inicio": "2025-08-11", "data_fim": "2026-06-26"}` para as 198 proposições salvas
- [x] 3.2 Testar cenário de banco vazio/sem proposições — confirmado por leitura de código (`periodo` vira `None` quando `MIN`/`MAX` retornam vazio, e `v-if="periodoTexto"` esconde a flag); não foi testado contra um banco vazio de fato, pois não é viável esvaziar os dados reais no Neon só para o teste
- [x] 3.3 Conferir responsividade da nova flag junto com "Última atualização" em mobile — testado com `npm run dev` + `flask run` reais, screenshot em 375px confirma as duas flags empilhadas e legíveis abaixo do título, sem overlap
