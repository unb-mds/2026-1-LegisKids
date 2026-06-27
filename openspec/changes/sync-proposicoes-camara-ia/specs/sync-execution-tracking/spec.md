## ADDED Requirements

### Requirement: Registro de cada execução do job em sync_executions
O sistema SHALL registrar uma entrada na tabela `sync_executions` para cada execução do job de sincronização, contendo: `id` (PK), `iniciado_em` (timestamp UTC), `finalizado_em` (timestamp UTC, nullable), `status` (enum: `em_andamento`, `concluido`, `concluido_parcial`, `erro_api`, `erro_interno`), `total_processados` (int), `total_inseridos` (int), `total_atualizados` (int), `total_erros` (int), `mensagem_erro` (text, nullable).

#### Scenario: Job inicia execução
- **WHEN** o Scheduler dispara `CamaraService.run_sync()`
- **THEN** o Repository insere uma linha em `sync_executions` com `status = 'em_andamento'`, `iniciado_em = now()` e contadores zerados

#### Scenario: Job conclui com sucesso
- **WHEN** `run_sync()` termina sem erros
- **THEN** a linha em `sync_executions` é atualizada com `status = 'concluido'`, `finalizado_em = now()` e os contadores finais corretos

#### Scenario: Job conclui com falhas parciais de categorização
- **WHEN** `run_sync()` termina mas algumas proposições foram salvas como `pendente_classificacao` por falha no Gemini
- **THEN** a linha em `sync_executions` é atualizada com `status = 'concluido_parcial'` e `total_erros` reflete o número de proposições com categorização falha

#### Scenario: Job falha por erro na API da Câmara
- **WHEN** as tentativas de retry à API da Câmara são esgotadas
- **THEN** a linha em `sync_executions` é atualizada com `status = 'erro_api'`, `finalizado_em = now()` e `mensagem_erro` com a descrição da exceção

#### Scenario: Job falha por erro interno inesperado
- **WHEN** uma exceção não tratada ocorre durante `run_sync()`
- **THEN** a linha em `sync_executions` é atualizada com `status = 'erro_interno'`, `finalizado_em = now()` e `mensagem_erro` com o traceback resumido

### Requirement: Consulta das últimas execuções via Repository
O Repository SHALL expor um método `get_ultimas_execucoes(limite: int)` que retorna as `N` últimas entradas de `sync_executions` ordenadas por `iniciado_em` DESC, para uso futuro em dashboards de monitoramento.

#### Scenario: Operador quer verificar histórico de execuções
- **WHEN** `CamaraRepository.get_ultimas_execucoes(10)` é chamado
- **THEN** retorna lista com até 10 execuções mais recentes, cada uma com todos os campos de `sync_executions`

### Requirement: Idempotência garantida pelo upsert transacional
O Repository SHALL implementar o upsert de proposições usando `INSERT ... ON CONFLICT (id_camara) DO UPDATE SET ...` em uma única transação por lote, de modo que reprocessar o mesmo conjunto de proposições produza exatamente o mesmo estado no banco.

#### Scenario: Job é reexecutado imediatamente após conclusão
- **WHEN** `run_sync()` é chamado duas vezes em sequência com os mesmos dados da API
- **THEN** a segunda execução tem `total_inseridos = 0` e `total_atualizados = 0` (nenhuma escrita desnecessária)

#### Scenario: Job é interrompido no meio e reexecutado
- **WHEN** `run_sync()` é interrompido após processar 50% das proposições e reexecutado
- **THEN** as proposições já processadas não são duplicadas e as restantes são inseridas/atualizadas corretamente
