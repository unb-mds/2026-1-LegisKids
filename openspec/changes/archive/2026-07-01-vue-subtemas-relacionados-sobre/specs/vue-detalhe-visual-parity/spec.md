## MODIFIED Requirements

### Requirement: Dados reais preenchem as seções correspondentes
As seções da tela com dado disponível na API (`ementa`, `sigla_partido`/`partido`, `subtemas`/`categorias`, `data_apresentacao`, `descricao_situacao`, `tramitacoes`, `id` para o link da ficha oficial) SHALL ser preenchidas com o dado real retornado por `GET /api/proposicoes/<id>`, nunca com valores de exemplo do spec visual original. A tela NÃO SHALL exibir campo de autor.

#### Scenario: Card "Sobre o projeto" usa a ementa real
- **WHEN** a proposição carregada tem `ementa` preenchida
- **THEN** o card "Sobre o projeto" exibe o texto da ementa real, com botão "Ver mais/Ver menos" alternando entre estado recolhido e expandido

#### Scenario: Sidebar de tramitação usa dado real
- **WHEN** a proposição tem itens em `tramitacoes`
- **THEN** a sidebar "Status da tramitação" renderiza uma timeline com os itens reais, ordenados cronologicamente

#### Scenario: Cabeçalho exibe todos os subtemas reais
- **WHEN** a proposição tem um ou mais itens em `categorias`
- **THEN** o cabeçalho exibe um badge colorido para cada subtema, usando a cor real de cada categoria

#### Scenario: Link para a ficha oficial da Câmara
- **WHEN** a proposição carregada tem um `id`
- **THEN** a tela exibe um link para `https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao=<id>`, construído sem depender de campo de backend adicional

### Requirement: Seções sem dado real exibem estado vazio explícito
Seções do spec visual sem correspondência na API hoje (objetivos do projeto, indicadores de análise, comentários) SHALL exibir um estado vazio explícito (reaproveitando a classe `.empty-state`) explicando que a informação não está disponível, e SHALL NUNCA exibir dados de exemplo ou fabricados como se fossem reais.

#### Scenario: Proposição sem indicadores de análise
- **WHEN** a proposição não tem dados de relevância/impacto/apoio popular (nenhuma proposição tem, hoje)
- **THEN** o card "Análise e indicadores" exibe um estado vazio informando que os indicadores ainda não estão disponíveis, em vez de barras com valores inventados

## ADDED Requirements

### Requirement: Projetos relacionados com dado real
O card "Projetos relacionados" SHALL buscar outras proposições reais via `GET /api/proposicoes`, priorizando o primeiro subtema da proposição atual; se não houver subtema ou a busca não retornar itens suficientes (após excluir a proposição atual), SHALL tentar buscar pelo `sigla_partido` da proposição atual. SHALL excluir a proposição atual dos resultados e limitar a até 3 itens. Na ausência de subtema, partido, ou resultados em ambos os critérios, SHALL exibir estado vazio.

#### Scenario: Relacionados por subtema
- **WHEN** a proposição atual tem subtema e existem outras proposições com o mesmo subtema
- **THEN** o card exibe até 3 proposições reais desse subtema, excluindo a proposição atual

#### Scenario: Fallback para partido
- **WHEN** a proposição atual não tem subtema, ou a busca por subtema não retorna itens além da própria proposição
- **THEN** o card tenta buscar por `sigla_partido` da proposição atual

#### Scenario: Nenhum relacionado disponível
- **WHEN** não há subtema nem partido disponíveis, ou nenhuma busca retorna resultados
- **THEN** o card exibe o estado vazio existente
