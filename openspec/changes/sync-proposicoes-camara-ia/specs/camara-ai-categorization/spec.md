## ADDED Requirements

### Requirement: Categorização automática de proposições via Gemini
O Service SHALL enviar a ementa de cada proposição ao Gemini (modelo `gemini-1.5-flash`) com um prompt estruturado contendo as categorias fixas disponíveis, e persistir a categoria retornada via Repository. A categoria SHALL ser uma das categorias fixas definidas na constante `CATEGORIAS_FIXAS` do Service; resposta fora do conjunto de categorias válidas SHALL ser tratada como falha e a proposição marcada como `pendente_classificacao`.

#### Scenario: Gemini retorna categoria válida
- **WHEN** o Gemini responde com uma string que corresponde exatamente a uma das entradas de `CATEGORIAS_FIXAS`
- **THEN** a proposição é associada à categoria retornada e `classificacao_status` é definido como `classificado`

#### Scenario: Gemini retorna categoria inválida ou não reconhecida
- **WHEN** o Gemini responde com texto que não corresponde a nenhuma entrada de `CATEGORIAS_FIXAS`
- **THEN** `classificacao_status` é definido como `pendente_classificacao` e um WARNING é emitido no log com a resposta recebida

#### Scenario: Proposição recebe múltiplas categorias
- **WHEN** o prompt permite múltiplas categorias e o Gemini retorna uma lista
- **THEN** a categoria com maior score de confiança é a primária (1:1) e as demais são associadas como secundárias via `proposicao_categorias`

### Requirement: Rate limit configurável para chamadas ao Gemini
O Service SHALL respeitar um limite de requisições por minuto ao Gemini, configurado via variável de ambiente `GEMINI_RATE_LIMIT_RPM` (padrão: 15 RPM). Ao atingir o limite, o Service SHALL aguardar o intervalo necessário antes de prosseguir, sem lançar erro.

#### Scenario: Volume de proposições excede o rate limit
- **WHEN** o lote de proposições a categorizar excede `GEMINI_RATE_LIMIT_RPM` por minuto
- **THEN** o Service introduz delay automático entre chamadas e prossegue sem erro, registrando INFO no log indicando o throttle

### Requirement: Fallback resiliente de categorização por IA
Falha no Gemini (timeout, erro de rede, cota esgotada) SHALL nunca bloquear o pipeline de ingestão. A proposição afetada SHALL ser salva com `classificacao_status = 'pendente_classificacao'` e o pipeline SHALL continuar com as demais proposições do lote.

#### Scenario: Gemini retorna timeout
- **WHEN** a chamada ao Gemini não responde em até 5 segundos
- **THEN** a proposição é salva com `classificacao_status = 'pendente_classificacao'`, um WARNING é emitido no log, e o processamento continua para a próxima proposição

#### Scenario: Cota do Gemini esgotada durante o lote
- **WHEN** o Gemini retorna erro de cota (429) para uma proposição do meio do lote
- **THEN** todas as proposições restantes do lote são salvas com `classificacao_status = 'pendente_classificacao'` e a execução do job é concluída com status `concluido_parcial`

#### Scenario: Módulo de IA completamente indisponível
- **WHEN** o `GOOGLE_API_KEY` não está configurado ou o módulo Gemini lança exceção na inicialização
- **THEN** todas as proposições do lote são salvas com `classificacao_status = 'pendente_classificacao'` e o pipeline de ingestão conclui normalmente sem categorização

### Requirement: Categorias fixas como constante no Service
O conjunto de categorias aceitas SHALL ser definido como constante `CATEGORIAS_FIXAS` no `camara_service.py`, cobrindo os temas de proteção infantil digital do LegisKids. O prompt enviado ao Gemini SHALL incluir a lista de categorias válidas para forçar resposta estruturada.

#### Scenario: Desenvolvedor adiciona nova categoria
- **WHEN** um desenvolvedor adiciona uma nova string à constante `CATEGORIAS_FIXAS`
- **THEN** o Gemini passa a usar a categoria nas próximas execuções sem nenhuma outra alteração de código
