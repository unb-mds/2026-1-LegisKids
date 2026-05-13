## ADDED Requirements

### Requirement: Dashboard interativo de produtividade
O sistema SHALL gerar `docs/performance/index.html` como um dashboard estático interativo para visualizar métricas de produtividade do GitHub do squad.

#### Scenario: Carregamento do dashboard
- **WHEN** o usuário abre `docs/performance/index.html`
- **THEN** o dashboard exibe KPIs, gráficos, filtros e tabelas com os dados gerados em `metrics.json`

#### Scenario: Funcionamento sem servidor
- **WHEN** o usuário abre o arquivo diretamente no navegador usando `file://`
- **THEN** os dados essenciais do relatório são exibidos sem erro de CORS ou chamada autenticada à API do GitHub

### Requirement: Filtros de análise
O dashboard SHALL permitir filtrar os dados por aluno, intervalo de datas e tipo de métrica.

#### Scenario: Filtro por aluno
- **WHEN** o usuário seleciona um ou mais alunos no filtro
- **THEN** os KPIs, gráficos e tabelas passam a considerar apenas os alunos selecionados

#### Scenario: Filtro por período
- **WHEN** o usuário altera o intervalo de datas
- **THEN** os gráficos temporais e tabelas detalhadas passam a exibir apenas eventos dentro do período selecionado

#### Scenario: Limpeza de filtros
- **WHEN** o usuário aciona a opção de limpar filtros
- **THEN** o dashboard volta a exibir todos os alunos e todo o período disponível

### Requirement: KPIs consolidados
O dashboard SHALL exibir cartões de resumo com métricas consolidadas do repositório e do conjunto filtrado.

#### Scenario: KPIs principais
- **WHEN** o dashboard é carregado com dados válidos
- **THEN** são exibidos totais de commits, issues, pull requests, reviews, itens abertos, itens fechados/mergeados e atividade recente

#### Scenario: KPIs atualizados por filtro
- **WHEN** o usuário altera qualquer filtro
- **THEN** os valores dos KPIs são recalculados para o conjunto filtrado

### Requirement: Gráficos comparativos por aluno
O dashboard SHALL exibir gráficos comparativos por aluno para commits, issues, pull requests, reviews e atividade recente.

#### Scenario: Comparação por aluno
- **WHEN** há métricas de mais de um aluno
- **THEN** os gráficos exibem os alunos lado a lado com valores proporcionais às métricas selecionadas

#### Scenario: Métrica sem dados
- **WHEN** a métrica selecionada não possui dados no período filtrado
- **THEN** o dashboard exibe uma mensagem de ausência de dados sem erro JavaScript

### Requirement: Gráficos temporais
O dashboard SHALL exibir evolução temporal das contribuições por semana ou mês.

#### Scenario: Timeline mensal
- **WHEN** o usuário seleciona a visualização mensal
- **THEN** o dashboard exibe commits, issues e pull requests agregados por mês

#### Scenario: Timeline semanal
- **WHEN** o usuário seleciona a visualização semanal
- **THEN** o dashboard exibe commits, issues e pull requests agregados por semana

### Requirement: Tabelas detalhadas
O dashboard SHALL exibir tabelas detalhadas e ordenáveis de alunos, commits, issues e pull requests.

#### Scenario: Tabela de alunos
- **WHEN** o dashboard é carregado
- **THEN** a tabela de alunos mostra nome, GitHub, commits, issues, pull requests, reviews, atividade recente e itens pendentes

#### Scenario: Ordenação de tabela
- **WHEN** o usuário clica no cabeçalho de uma coluna ordenável
- **THEN** a tabela é reordenada por aquela coluna alternando entre ordem crescente e decrescente

#### Scenario: Busca textual
- **WHEN** o usuário digita no campo de busca
- **THEN** as tabelas detalhadas exibem apenas linhas que correspondem ao texto buscado

### Requirement: Links auditáveis para o GitHub
O dashboard SHALL incluir links para itens do GitHub quando houver URL disponível nos dados.

#### Scenario: Link de issue ou pull request
- **WHEN** uma tabela exibe uma issue ou pull request com URL do GitHub
- **THEN** o número ou título do item é renderizado como link para a página correspondente no GitHub

### Requirement: Segurança dos dados renderizados
O dashboard SHALL não incluir tokens, credenciais ou cabeçalhos de autenticação no HTML ou no JSON público.

#### Scenario: Arquivos sem token
- **WHEN** `docs/performance/index.html` e `docs/performance/metrics.json` são inspecionados após a geração
- **THEN** não há ocorrência do valor de `GITHUB_TOKEN` nem de cabeçalhos `Authorization`
