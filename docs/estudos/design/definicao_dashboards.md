# Definição de Dashboards do Sistema
O sistema irá consumir dados da API pública da Câmara dos Deputados.

O objetivo do sistema é coletar e analisar projetos de lei relacionados à **segurança da criança na internet**, permitindo visualização acadêmica de:

- tendências legislativas;
- atuação política;
- tramitação dos projetos;
- temas mais discutidos.

O sistema armazenará no máximo **200 MB de dados**, utilizando PostgreSQL e um conjunto reduzido de tabelas relacionais.

Por isso, os dashboards precisam ser:

- relevantes para análise acadêmica;
- simples de implementar;
- compatíveis com os dados da API;
- leves em armazenamento e processamento.

Cada dashboard será sinalizado usando o método MoSCoW (Must, Should, Could, Wish), e:

- Must: deverá estar no projeto.
- Should: estará no projeto, mas será dada menor prioridade.
- Could: se tivermos tempo, podemos aplicar.
- Wish: num mundo hipotético, usaríamos.

# Dashboards Selecionados

Após análise do escopo do projeto, os dashboards mais relevantes são:

| Dashboard | Objetivo |
| --- | --- |
| Dashboard 1 | Panorama Geral |
| Dashboard 2 | Evolução Temporal |
| Dashboard 3 | Análise Política |
| Dashboard 4 | Tramitação Legislativa |
| Dashboard 5 | Análise de Conteúdo |

Esses cinco dashboards cobrem praticamente todos os objetivos analíticos do sistema sem adicionar complexidade desnecessária.

# Dashboard 1 — Panorama Geral

## Objetivo

Apresentar uma visão rápida do cenário legislativo relacionado à segurança da criança na internet.

Esse será o dashboard inicial do sistema.

## Dados Utilizados

Endpoint:

- `/proposicoes`

Campos:

- `id`
- `siglaTipo`
- `numero`
- `ano`
- `ementa`
- `dataApresentacao`
- `statusProposicao.descricaoSituacao`

## Componentes

### Total de Projetos (Must)

Quantidade total de projetos armazenados.

### Projetos em Tramitação (Must)

Projetos com situação ativa.

### Projetos Arquivados (Should)

Projetos encerrados ou arquivados.

### Projetos Aprovados (Should)

Projetos aprovados pela Câmara.

### Projetos por Ano (Must)

Tipo:

- gráfico de linha.

Objetivo:

- visualizar crescimento do tema ao longo do tempo.

### Distribuição por Status (Should)

Tipo:

- gráfico donut.

Categorias:

- em tramitação;
- arquivado;
- aprovado;
- outros.

Objetivo:

- apresentar situação geral das proposições.

### Últimos Projetos Adicionados (Should)

Tipo:

- tabela.

Colunas:

- número;
- ano;
- ementa;
- status;
- data de apresentação.

Objetivo:

- acompanhar proposições recentes.

# Dashboard 2 — Evolução Temporal (Must)

## Objetivo

Identificar tendências legislativas relacionadas ao tema.

## Dados Utilizados

Endpoint:

- `/proposicoes`

Campos:

- `dataApresentacao`
- `ano`

## Componentes

### Projetos por Mês (Must)

Tipo:

- gráfico de linha temporal.

Objetivo:

- detectar períodos de maior atividade legislativa.

### Crescimento Anual (Should)

Tipo:

- gráfico de barras.

Objetivo:

- comparar quantidade de projetos entre anos.

### Média Mensal de Proposições (Could)

Tipo:

- KPI numérico.

Objetivo:

- medir frequência média de criação de projetos.

### Heatmap de Atividade Legislativa (Could)

Tipo:

- mapa de calor.

Objetivo:

- identificar meses e anos com maior atividade.

# Dashboard 3 — Análise Política (Must)

## Objetivo

Identificar quais grupos políticos mais atuam no tema.

## Dados Utilizados

Endpoints:

- `/proposicoes`
- `/partidos`

Campos:

- proposicao;
- partido;

## Componentes

### Projetos por Partido (Should)

Tipo:

- gráfico de barras horizontais.

Objetivo:

- identificar protagonismo partidário.

### Comparação Partido × Status (Could)

Tipo:

- barras empilhadas.

Objetivo:

- comparar efetividade legislativa entre partidos.

# Considerações Técnicas

Os dashboards foram escolhidos para:

- utilizar poucos dados;
- evitar processamento pesado;
- evitar relações muito complicadas;
- funcionar com baixo custo computacional;
- aproveitar diretamente os dados da API da Câmara;
- facilitar desenvolvimento acadêmico.

O sistema não necessitará de Big Data, processamento distribuído ou infraestrutura complexa.

# Conclusão

Os dashboards selecionados são suficientes para atender os objetivos acadêmicos do projeto sem adicionar complexidade excessiva.

Eles permitem:

- monitorar atividade legislativa;
- identificar tendências;
- analisar atuação política;
- acompanhar tramitação;
- explorar os temas discutidos nos projetos.

Além disso, os dashboards foram escolhidos considerando simplicidade de implementação, desempenho e limitação de armazenamento.