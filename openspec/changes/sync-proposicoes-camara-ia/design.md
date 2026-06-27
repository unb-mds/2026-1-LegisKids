## Context

O LegisKids não possui hoje nenhum job automatizado de ingestão de dados. As proposições da Câmara são acessadas pontualmente via chamadas manuais ao backend. Para viabilizar buscas, alertas e análises históricas, é necessário um pipeline regular que sincronize o banco com a API `dadosabertos.camara.leg.br/api/v2`, normalize os dados, categorize via Gemini e registre a execução.

A arquitetura do projeto já separa routes/services/models; este pipeline deve seguir a mesma separação de camadas, adicionando `schedulers/` e `repositories/` como módulos próprios dentro de `backend/src/`.

## Goals / Non-Goals

**Goals:**
- Sincronização idempotente e periódica de proposições (novas e alteradas)
- Categorização automática via Gemini com fallback resiliente
- Registro de cada execução do job para auditoria e monitoramento
- Retry automático para falhas transitórias da API da Câmara
- Logs estruturados e claros em cada fase do pipeline

**Non-Goals:**
- Sincronização em tempo real (webhook/streaming)
- Autenticação ou autorização de usuários
- Exposição de endpoints REST para acionar o job (apenas CLI e scheduler interno)
- Categorização manual de proposições
- Coleta de dados além de proposições (ex.: votações, discursos)

## Decisions

### D1: APScheduler para agendamento (não Celery)

**Decisão:** usar `APScheduler` (background scheduler in-process) em vez de Celery + Redis.

**Rationale:** o job roda dentro do mesmo processo Flask, sem necessidade de workers externos nem broker de mensagens. APScheduler é suficiente para execuções periódicas simples e reduz a complexidade operacional. Se no futuro o volume exigir filas distribuídas, a interface do Scheduler pode ser trocada sem alterar Service ou Repository.

**Alternativa descartada:** Celery — overhead de infraestrutura (Redis/RabbitMQ) desproporcional para o volume atual.

### D2: Retry via `tenacity` (não retry caseiro)

**Decisão:** usar `tenacity` para retry com backoff exponencial nas chamadas à API da Câmara e ao Gemini.

**Rationale:** `tenacity` provê controle fino sobre número de tentativas, delays, jitter e condições de parada, sem código repetitivo. Configurável por variável de ambiente.

**Alternativa descartada:** `urllib3.Retry` — funciona apenas em nível de conexão HTTP, não cobre erros de negócio (ex.: resposta 503 ou corpo inválido).

### D3: Upsert transacional no Repository (INSERT ... ON CONFLICT)

**Decisão:** o Repository usa `INSERT INTO proposicoes (...) ON CONFLICT (id_camara) DO UPDATE SET ...` em uma única transação por lote.

**Rationale:** garante idempotência e atomicidade. Se o job for interrompido no meio, reprocessar o mesmo lote não gera duplicatas nem estados parciais.

**Alternativa descartada:** SELECT + INSERT/UPDATE separados — sujeito a race condition e duplicidade em reruns.

### D4: Fallback IA → `pendente_classificacao`

**Decisão:** se o Gemini falhar (timeout, erro de rede, limite de cota) a proposição é salva com `classificacao_status = 'pendente_classificacao'`. Um job periódico separado (fora do escopo desta mudança) poderá reclassificar esses registros.

**Rationale:** falha no módulo de IA não deve bloquear a ingestão de dados legislativos. Os dados ficam disponíveis; a categorização é eventual.

**Alternativa descartada:** abortar o upsert se a IA falhar — penalizaria toda a execução por falha em um subconjunto.

### D5: Categorias fixas definidas em constante no Service

**Decisão:** as categorias aceitas pelo Gemini são definidas como constante (`CATEGORIAS_FIXAS`) no `camara_service.py`, não em banco.

**Rationale:** as categorias do LegisKids são estáveis e orientadas ao domínio (proteção infantil digital). Torná-las dinâmicas (via tabela) adicionaria complexidade sem benefício imediato. Quando precisarem mudar, basta editar a constante e criar migration para corrigir categorizações antigas.

### D6: Camadas sem cruzamento

```
Scheduler → Service → Repository
               ↓
           Gemini API
               ↓
           API Câmara
```

- **Scheduler:** nenhuma importação de modelos SQLAlchemy ou acesso a banco. Apenas chama `Service.run_sync()`.
- **Service:** contém toda a lógica de negócio e chamadas externas. Nunca acessa a sessão SQLAlchemy diretamente.
- **Repository:** único ponto de escrita no banco. Recebe DTOs validados, executa SQL/ORM.

## Risks / Trade-offs

| Risco | Mitigação |
|---|---|
| API da Câmara retorna volume muito alto (milhares de proposições por execução) | Paginação com `itens=100` por página; rate limit configurável no Service |
| Gemini atinge cota de requisições | `GEMINI_RATE_LIMIT_RPM` controla o throttle; fallback para `pendente_classificacao` |
| APScheduler perde jobs após reinício do processo Flask | Aceitável em dev; em produção, usar `misfire_grace_time` e `coalesce=True`; monitorar via `sync_executions` |
| Mudança de schema da API da Câmara | Validação explícita de campos obrigatórios no Service; campos desconhecidos ignorados |
| Concorrência: dois processos rodando o job simultaneamente | APScheduler in-process garante execução única por processo; se multi-instância, usar advisory lock no PostgreSQL (fora do escopo inicial) |

## Migration Plan

1. Criar e aplicar migration para a tabela `sync_executions` e coluna `classificacao_status` em `proposicoes`.
2. Instalar dependências novas: `APScheduler`, `tenacity`.
3. Registrar o scheduler no `create_app()` do Flask app factory.
4. Verificar variáveis de ambiente necessárias no `.env.example`.
5. Executar `flask sync-camara` (comando CLI) manualmente para validar primeira execução.

**Rollback:** desregistrar o scheduler do app factory e remover a migration (down). Sem impacto em dados já existentes.

## Open Questions

- O endpoint `/proposicoes` da API da Câmara deve ser filtrado por tema/palavra-chave na query, ou trazer tudo e filtrar no Service? → Por ora, filtrar na query com as palavras-chave definidas no CLAUDE.md para reduzir volume.
- O job de reclassificação de `pendente_classificacao` deve ser parte desta mudança ou de uma mudança separada? → Separado (escopo fora desta mudança; mencionado em US-AI-RESILIÊNCIA).
