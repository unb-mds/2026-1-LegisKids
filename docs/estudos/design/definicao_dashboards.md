# Definição de Dashboards do Sistema

O sistema irá consumir dados da API pública da Câmara dos Deputados com o objetivo de coletar e analisar projetos de lei relacionados à segurança da criança na internet, permitindo visualização acadêmica de tendências legislativas, atuação política, tramitação dos projetos e temas mais discutidos.

O sistema armazenará no máximo 200 MB de dados, utilizando PostgreSQL e um conjunto reduzido de tabelas relacionais. Por isso, os dashboards precisam ser relevantes para análise acadêmica, simples de implementar, compatíveis com os dados da API e leves em armazenamento e processamento.

Cada dashboard é classificado pelo método MoSCoW:

- **Must** — deverá estar no projeto
- **Should** — poderá estar no projeto, com menor prioridade
- **Could** — será aplicado se houver tempo
- **Wish** — num cenário ideal, seria implementado

---

## Dashboards selecionados

| Dashboard | Objetivo |
| --- | --- |
| Dashboard 1 | Panorama Geral |
| Dashboard 2 | Evolução Temporal |
| Dashboard 3 | Análise Política |
| Dashboard 4 | Tramitação Legislativa |
| Dashboard 5 | Análise de Conteúdo |

Esses cinco dashboards cobrem praticamente todos os objetivos analíticos do sistema sem adicionar complexidade desnecessária.

---

## Dashboard 1 — Panorama Geral (Must)

Visão rápida do cenário legislativo relacionado ao tema. Será o dashboard inicial do sistema.

### Dados utilizados

Endpoint: `/proposicoes`

Campos: `id`, `siglaTipo`, `numero`, `ano`, `ementa`, `dataApresentacao`, `statusProposicao.descricaoSituacao`

### Componentes

**Cards informativos** — total de projetos armazenados, projetos em tramitação, projetos arquivados e projetos aprovados.

**Projetos por ano** — gráfico de linha para visualizar o crescimento do tema ao longo do tempo.

**Distribuição por status** — gráfico donut com categorias: em tramitação, arquivado, aprovado e outros.

**Últimos projetos adicionados** — tabela com número, ano, ementa, autor, status e data de apresentação.

---

## Dashboard 2 — Evolução Temporal (Must)

Identificar tendências legislativas relacionadas ao tema.

### Dados utilizados

Endpoint: `/proposicoes`

Campos: `dataApresentacao`, `ano`

### Componentes

**Projetos por mês** — gráfico de linha temporal para detectar períodos de maior atividade legislativa.

**Crescimento anual** — gráfico de barras para comparar quantidade de projetos entre anos.

**Média mensal de proposições** — KPI numérico para medir frequência média de criação de projetos.

**Heatmap de atividade legislativa** — mapa de calor para identificar meses e anos com maior atividade.

---

## Dashboard 3 — Análise Política (Must)

Identificar quais grupos políticos mais atuam no tema.

### Dados utilizados

Endpoints: `/proposicoes`, `/deputados`, `/partidos`

Campos: autor, partido, UF

### Componentes

**Projetos por partido** — gráfico de barras horizontais para identificar protagonismo partidário.

**Projetos por estado** — mapa do Brasil ou gráfico de barras para visualizar distribuição regional.

**Ranking de deputados** — tabela ordenada com deputado, partido, UF e quantidade de projetos.

**Comparação partido × status** — barras empilhadas para comparar efetividade legislativa entre partidos.

---

## Considerações técnicas

Os dashboards foram escolhidos para utilizar poucos dados, evitar processamento pesado, funcionar com baixo custo computacional e facilitar o desenvolvimento acadêmico. O sistema não necessitará de Big Data, processamento distribuído ou infraestrutura complexa.

---

## Conclusão

Os dashboards selecionados são suficientes para atender os objetivos acadêmicos do projeto sem adicionar complexidade excessiva, permitindo monitorar atividade legislativa, identificar tendências, analisar atuação política, acompanhar tramitação e explorar os temas discutidos nos projetos.