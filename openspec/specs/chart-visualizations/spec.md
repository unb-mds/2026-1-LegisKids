# Spec: chart-visualizations

## Objetivo

Definir os componentes de visualização de dados usando Chart.js 4, cobrindo gráficos de barras (subtemas), linha temporal e rosca (status) — preparação para US11, US12, US13.

## Contexto

O LegisKids usa Chart.js 4 para gráficos convencionais (barras, linha, rosca). Os componentes vivem em `src/components/charts/`, consomem dados via props vindos dos services e destroem a instância no unmount para evitar vazamento de memória.

## Escopo

- `GraficoSubtemas.vue` — barras verticais por subtema
- `GraficoTemporal.vue` — linha de evolução temporal
- `GraficoStatus.vue` — rosca de distribuição por status
- Estado vazio ("Nenhum dado disponível") para todos
- Acessibilidade: `aria-label` e `role="img"` nos canvas

## Requisitos

### Requirement: Componente de gráfico de barras por subtema
O sistema SHALL possuir o componente `src/components/charts/GraficoSubtemas.vue` que recebe dados e renderiza um gráfico de barras verticais com Chart.js.

#### Scenario: Gráfico renderizado com dados
- **WHEN** o componente recebe dados `{ subtemas: ['Cyberbullying', 'Privacidade'], totais: [42, 18] }`
- **THEN** um gráfico de barras é renderizado em um `<canvas>` com os rótulos e valores correspondentes

#### Scenario: Gráfico com zero resultados
- **WHEN** o endpoint retorna lista vazia
- **THEN** o componente exibe mensagem "Nenhum dado disponível" em vez de um gráfico vazio

#### Scenario: Gráfico destrói instância ao desmontar
- **WHEN** o componente é desmontado (ex: usuário navega para outra página)
- **THEN** a instância Chart.js é destruída via `chart.destroy()` para evitar vazamento de memória

### Requirement: Componente de gráfico de linha temporal
O sistema SHALL possuir o componente `src/components/charts/GraficoTemporal.vue` que recebe séries temporais do backend e renderiza evolução do número de proposições ao longo do tempo.

#### Scenario: Linha temporal renderizada
- **WHEN** o componente recebe dados `{ meses: ['Jan/26', 'Fev/26'], contagens: [12, 25] }`
- **THEN** um gráfico de linha é renderizado mostrando a evolução temporal

### Requirement: Componente de gráfico de rosca por status
O sistema SHALL possuir o componente `src/components/charts/GraficoStatus.vue` que renderiza a distribuição das proposições por status como gráfico de rosca.

#### Scenario: Distribuição de status renderizada
- **WHEN** o componente recebe `{ labels: ['Em tramitação', 'Aprovado'], values: [30, 10] }`
- **THEN** um gráfico de rosca é renderizado com cores distintas para cada status

### Requirement: Acessibilidade mínima nos gráficos
Cada componente de gráfico SHALL incluir um atributo `aria-label` descritivo no elemento `<canvas>` e `role="img"`.

#### Scenario: Gráfico acessível por leitores de tela
- **WHEN** um leitor de tela acessa o componente de gráfico
- **THEN** o `aria-label` descreve o tipo e propósito do gráfico (ex: "Gráfico de barras: proposições por subtema")
