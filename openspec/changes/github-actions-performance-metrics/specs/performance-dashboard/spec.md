## ADDED Requirements

### Requirement: HTML estático gerado a partir do metrics.json
O script SHALL gerar `docs/performance/index.html` como um arquivo HTML autossuficiente que lê dados do `metrics.json` embutidos inline (ou via fetch relativo), sem necessidade de servidor.

#### Scenario: Abertura direta no navegador
- **WHEN** o usuário abre `docs/performance/index.html` diretamente no navegador (protocolo `file://`)
- **THEN** a página exibe o relatório com dados dos alunos sem erro de rede ou CORS

### Requirement: Gráfico de commits por aluno
O dashboard SHALL exibir um gráfico de barras com o total de commits por aluno.

#### Scenario: Gráfico renderizado com dados reais
- **WHEN** `metrics.json` contém alunos com `commits_count > 0`
- **THEN** o gráfico exibe uma barra por aluno com altura proporcional ao número de commits

#### Scenario: Gráfico sem dados
- **WHEN** todos os alunos têm `commits_count: 0`
- **THEN** o gráfico exibe mensagem indicando ausência de dados, sem erro JavaScript

### Requirement: Gráfico de issues por aluno
O dashboard SHALL exibir um gráfico de barras com o total de issues criadas por aluno.

#### Scenario: Gráfico de issues renderizado
- **WHEN** `metrics.json` contém alunos com `issues_count > 0`
- **THEN** o gráfico exibe uma barra por aluno com altura proporcional ao número de issues

### Requirement: Tabela de resumo por aluno
O dashboard SHALL exibir uma tabela com, por aluno: nome, login GitHub, total de commits, total de issues, total de caracteres em issues e média de caracteres por issue.

#### Scenario: Tabela completa
- **WHEN** a página é carregada com `metrics.json` válido
- **THEN** a tabela contém uma linha por aluno com todos os seis campos preenchidos

### Requirement: Uso de Chart.js via CDN
O dashboard SHALL carregar Chart.js de CDN (`https://cdn.jsdelivr.net/npm/chart.js`) para renderização dos gráficos.

#### Scenario: Script CDN presente no HTML
- **WHEN** o arquivo `index.html` gerado é inspecionado
- **THEN** contém uma tag `<script>` com `src` apontando para o CDN do Chart.js

### Requirement: Nenhum token ou dado sensível no HTML
O dashboard SHALL não incluir o `GITHUB_TOKEN` ou qualquer credencial no HTML ou nos dados embutidos.

#### Scenario: HTML sem token
- **WHEN** o conteúdo de `index.html` é inspecionado após a geração
- **THEN** não há ocorrência do valor do `GITHUB_TOKEN` no arquivo

### Requirement: Indicação de data de geração do relatório
O dashboard SHALL exibir o campo `generated_at` do `metrics.json` na página, informando quando os dados foram coletados.

#### Scenario: Data visível na página
- **WHEN** a página é carregada
- **THEN** a data/hora de geração é visível no cabeçalho ou rodapé da página
