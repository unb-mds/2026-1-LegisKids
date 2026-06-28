# Relatório — feat/gemini-classificacao-neon

**Branch:** `feat/gemini-classificacao-neon`
**Base:** `develop`
**Commits exclusivos:** 8
**Testes:** 39/39 passando

---

## O que foi implementado

### 1. Pipeline de classificação Gemini + persistência no Neon (`ce29c42`)
- Integração completa: API da Câmara → filtro → Gemini → PostgreSQL (Neon)
- Modelo `SyncExecution` para registrar cada execução de sync com contadores e status
- Comando CLI `flask sync-camara` para execução manual
- Categorias fixas (8): cyberbullying, exploração sexual infantil online, proteção de dados de menores, segurança digital infantil, regulação de plataformas digitais, conteúdos nocivos para menores, crimes virtuais contra crianças, privacidade de menores
- Seed automático das categorias na inicialização
- Proposições irrelevantes ao tema são descartadas antes de serem salvas

### 2. Troca de SDK Gemini (`ecf67d5`)
- Migração de `google-generativeai` para `google-genai 2.10.0`
- Modelo: `gemini-2.5-flash` (disponível na tier gratuita)
- Timeout de 60s por chamada

### 3. Otimizações de consumo e classificação (`45187d0`)
- **Classificação em lote:** N ementas por chamada ao Gemini (padrão: 10, configurável via `GEMINI_BATCH_SIZE`)
- **Múltiplas categorias por proposição:** o Gemini pode retornar 1 a N categorias válidas por ementa
- **Filtro de data:** consumo de proposições a partir de `2022-01-01` (`CAMARA_DATA_INICIO`)
- **Retry para erro 429** (cota esgotada): aguarda 60s e re-tenta (até 3 tentativas)
- **Re-tentativa de pendentes:** `_retentar_pendentes()` reclassifica proposições com `pendente_classificacao` no início de cada run

### 4. Limpeza do backend (`42703c8`)
- Remoção de `src/backend/main.py` (CLI com `input()` em nível de módulo — bloqueava testes)
- Remoção de `src/backend/services/camara_api.py` (duplicata da camada de serviço)
- Correção de `datetime.utcnow` deprecated → `datetime.now(timezone.utc)` em todos os modelos

### 5. Filtro de reprocessamento (`bce7a8b`)
- **Early-stop de paginação:** se todos os IDs de uma página já existem no banco, encerra a paginação (a API retorna em ordem DESC por ID, então páginas seguintes seriam ainda mais antigas)
- **Skip antes do Gemini:** IDs já conhecidos são filtrados antes de qualquer chamada ao Gemini
- **`get_ids_existentes()`** no repositório: query única `SELECT id WHERE id IN (...)` por página

### 6. Retry para erro 503 (`237bdc9`)
- `_is_transient_error()`: detecta erros 503 / "unavailable" do Gemini
- Aguarda 30s e re-tenta (até 3 tentativas, igual ao 429)
- Isolamento de testes: mocks de `get_proposicoes_pendentes` para evitar interferência do estado real do banco

### 7. Scheduler cron diário (`32efd48`)
- Troca de `trigger="interval"` por `trigger="cron"` com `hour=12, minute=0`
- Configurável via `CAMARA_SYNC_HOUR` e `CAMARA_SYNC_MINUTE` no `.env`
- `coalesce=True` + `misfire_grace_time=300s` para robustez

### 8. Auditoria pré-develop (`876ad11`)
- **Bug corrigido:** `cota_gemini_esgotada` era código morto — `_classificar_lote()` nunca lançava exceção; agora detectado via `all(resultado is None)`
- **Bug corrigido:** `total_descartados` não era persistido — adicionado ao modelo `SyncExecution` + migration
- **Migration `ded4438e4a2c`:** coluna `total_descartados`, índice `idx_proposicoes_classificacao_status`, alinhamento de índices e constraints com o Neon real
- **Limpeza:** remoção de `src/backend/migrations/testa_tabelas.py`

---

## Variáveis de ambiente adicionadas

| Variável | Padrão | Descrição |
|---|---|---|
| `GOOGLE_API_KEY` | — | Chave da API do Gemini (obrigatória) |
| `CAMARA_DATA_INICIO` | `2022-01-01` | Data de início para busca de proposições |
| `GEMINI_BATCH_SIZE` | `10` | Proposições por chamada ao Gemini |
| `CAMARA_SYNC_HOUR` | `12` | Hora do sync diário |
| `CAMARA_SYNC_MINUTE` | `0` | Minuto do sync diário |

---

## Migrations aplicadas (nesta branch)

| Revisão | O que faz |
|---|---|
| `ca57241159f9` | Cria `sync_executions`; adiciona `classificacao_status` em `proposicoes` |
| `f3a1b2c4d5e6` | Garante `categorias` e `proposicao_categoria` com CASCADE |
| `ded4438e4a2c` | Adiciona `total_descartados`; cria índice em `classificacao_status`; alinha constraints |

---

## O que está completo

- [x] Leitura paginada da API da Câmara (com filtro de data, palavras-chave e paginação DESC)
- [x] Classificação em lote pelo Gemini (múltiplas categorias, retry 429/503, fallback para pendente)
- [x] Persistência idempotente no Neon via upsert (`ON CONFLICT DO UPDATE`)
- [x] Relacionamento N:N proposições ↔ categorias (`proposicao_categoria`)
- [x] Re-tentativa automática de proposições pendentes a cada run
- [x] Early-stop + skip de IDs já conhecidos (evita reprocessamento)
- [x] Scheduler cron diário ao meio-dia (enquanto Flask estiver no ar)
- [x] Registro de cada execução em `sync_executions` com contadores e status
- [x] Testes de integração: 39/39 passando

---

## O que está pendente

### Nesta branch / pré-develop
- [ ] **Scheduler sem servidor 24/7:** o scheduler só roda enquanto `flask run` estiver ativo. Para garantir o sync diário de forma confiável, é necessário ou um servidor sempre ligado ou um GitHub Actions cron chamando um endpoint `POST /sync`.

### Próximas releases (fora do escopo desta branch)
- [ ] Endpoints REST para o frontend consumir proposições, categorias e estatísticas (`src/backend/routes/` está vazio)
- [ ] Atualização de tramitações (job diário separado do sync de novas proposições)
- [ ] Autenticação Google OAuth 2.0
- [ ] Favoritos, histórico de buscas, alertas
- [ ] Exportação CSV/PDF

---

## Estado geral para o merge

O backend de coleta, classificação e persistência está funcional e testado. O único ponto em aberto antes do merge para `develop` é decidir como garantir o scheduler sem depender do Flask estar no ar — mas isso pode ser resolvido em uma issue separada sem bloquear o merge.
