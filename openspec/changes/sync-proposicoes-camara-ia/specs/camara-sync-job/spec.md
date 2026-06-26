## ADDED Requirements

### Requirement: Job de sincronização agendado e executável manualmente
O sistema SHALL possuir um job de sincronização que busca proposições da API da Câmara (`dadosabertos.camara.leg.br/api/v2`), identifica registros novos e alterados, e persiste as proposições válidas no banco de dados via Repository. O job SHALL ser executado automaticamente em intervalo configurável (variável de ambiente `CAMARA_SYNC_INTERVAL_MINUTES`) e também sob demanda via comando CLI (`flask sync-camara`).

#### Scenario: Job executa automaticamente no intervalo configurado
- **WHEN** a aplicação Flask está em execução e o intervalo configurado transcorre
- **THEN** o Scheduler dispara `CamaraService.run_sync()` sem intervenção manual e registra a execução em `sync_executions`

#### Scenario: Operador dispara sync manualmente via CLI
- **WHEN** o operador executa `flask sync-camara` no terminal
- **THEN** o Service executa a sincronização completa e imprime resumo no stdout (total processado, inserido, atualizado, erros)

#### Scenario: Job identifica proposição nova
- **WHEN** a API retorna uma proposição cujo `id` da Câmara não existe em `proposicoes`
- **THEN** a proposição é inserida e o contador `total_inseridos` da execução é incrementado

#### Scenario: Job identifica proposição alterada
- **WHEN** a API retorna uma proposição cujo `id` da Câmara já existe em `proposicoes` mas com campos diferentes (ex.: `status_atual`)
- **THEN** os campos alterados são atualizados e o contador `total_atualizados` da execução é incrementado

#### Scenario: Job recebe proposição idêntica à já existente
- **WHEN** a API retorna uma proposição cujos dados são idênticos ao registro em banco
- **THEN** nenhuma escrita é realizada e os contadores `total_inseridos` e `total_atualizados` permanecem inalterados (idempotência)

### Requirement: Retry automático para falhas transitórias da API da Câmara
O Service SHALL realizar no mínimo 3 tentativas com backoff exponencial ao encontrar erros HTTP 5xx, timeout ou falha de rede nas chamadas à API da Câmara. Após esgotar as tentativas, a exceção SHALL ser registrada no log e a execução atual marcada com status `erro_api`.

#### Scenario: API retorna 504 na primeira tentativa
- **WHEN** a chamada à API da Câmara retorna HTTP 504
- **THEN** o Service aguarda o intervalo de backoff e retenta a chamada até 3 vezes antes de falhar

#### Scenario: Todas as tentativas falham
- **WHEN** as 3 tentativas à API da Câmara são esgotadas sem sucesso
- **THEN** a execução do job é marcada como `erro_api` em `sync_executions` com a mensagem de erro registrada

### Requirement: Separação estrita de camadas no pipeline de sync
O Scheduler SHALL chamar apenas o Service; o Service SHALL chamar apenas o Repository para escrita em banco; o Repository SHALL ser o único módulo a acessar a sessão SQLAlchemy diretamente. Nenhuma dessas camadas SHALL importar ou depender das demais de forma cruzada (ex.: Scheduler não importa modelos ORM; Service não usa Session diretamente).

#### Scenario: Adição de novo endpoint da Câmara no futuro
- **WHEN** um desenvolvedor precisa sincronizar um novo tipo de dado da API da Câmara
- **THEN** adiciona um método no Service e um método no Repository sem modificar o Scheduler ou o app factory

### Requirement: Logs estruturados em cada fase do pipeline
O Service SHALL emitir logs nos níveis apropriados (`INFO`/`WARNING`/`ERROR`) para: início da execução, total de páginas buscadas, total processado por página, cada erro individual de proposição, e resumo final (totais inseridos/atualizados/erros).

#### Scenario: Execução bem-sucedida completa
- **WHEN** o job finaliza sem erros
- **THEN** o log contém: mensagem de início com timestamp, progresso por página, e resumo final com totais de inseridos, atualizados e processados

#### Scenario: Proposição individual falha na validação
- **WHEN** uma proposição retornada pela API não passa na validação de campos obrigatórios
- **THEN** o log emite WARNING com o `id` da proposição e o campo inválido, e a execução continua para as demais proposições
