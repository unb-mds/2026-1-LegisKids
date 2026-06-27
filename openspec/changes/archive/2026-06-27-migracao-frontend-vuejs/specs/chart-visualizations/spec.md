## ADDED Requirements

### Requirement: Componente de gráfico de barras por subtema
O sistema SHALL possuir o componente `src/components/charts/GraficoSubtemas.vue` que recebe dados do endpoint `/api/proposicoes/por-subtema` e renderiza um gráfico de barras verticais com Chart.js, mostrando a quantidade de proposições por subtema (preparação para US13/US11).

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
O sistema SHALL possuir o componente `src/components/charts/GraficoTemporal.vue` que recebe séries temporais do backend e renderiza evolução do número de proposições ao longo do tempo (preparação para US11/US12).

#### Scenario: Linha temporal renderizada
- **WHEN** o componente recebe dados `{ meses: ['Jan/26', 'Fev/26'], contagens: [12, 25] }`
- **THEN** um gráfico de linha é renderizado mostrando a evolução temporal

### Requirement: Componente de gráfico de rosca por status
O sistema SHALL possuir o componente `src/components/charts/GraficoStatus.vue` que renderiza a distribuição das proposições por status (Em tramitação, Aprovado, Arquivado) como gráfico de rosca (preparação para US13).

#### Scenario: Distribuição de status renderizada
- **WHEN** o componente recebe `{ labels: ['Em tramitação', 'Aprovado'], values: [30, 10] }`
- **THEN** um gráfico de rosca é renderizado com cores distintas para cada status

### Requirement: Acessibilidade mínima nos gráficos
Cada componente de gráfico SHALL incluir um atributo `aria-label` descritivo no elemento `<canvas>` e um texto alternativo visível para leitores de tela.

#### Scenario: Gráfico acessível por leitores de tela
- **WHEN** um leitor de tela acessa o componente de gráfico
- **THEN** o `aria-label` descreve o tipo e propósito do gráfico (ex: "Gráfico de barras: proposições por subtema")
