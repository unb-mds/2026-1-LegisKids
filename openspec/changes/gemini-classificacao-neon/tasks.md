## 1. Seed de categorias

- [x] 1.1 Adicionar constante `SEED_CATEGORIAS` em `camara_repository.py` com as 8 categorias (nome, descrição, cor hex, ícone)
- [x] 1.2 Implementar `seed_categorias()` em `camara_repository.py` usando `INSERT INTO categorias ... ON CONFLICT (nome) DO NOTHING` via SQLAlchemy Core
- [x] 1.3 Adicionar cache em memória `_cache_categorias: dict[str, int] = {}` para lookup de `categoria_id` por nome
- [x] 1.4 Implementar `_get_categoria_id(nome) -> int | None` que popula o cache na primeira chamada
- [x] 1.5 Chamar `seed_categorias()` em `app.py` dentro do `with app.app_context()` após `db.init_app(app)`, antes de iniciar o scheduler

## 2. Vinculação proposicao → categoria

- [x] 2.1 Implementar `vincular_categoria(proposicao_id: int, categoria_nome: str) -> None` em `camara_repository.py`
      — faz lookup do id via `_get_categoria_id`, insere em `proposicao_categoria` com `ON CONFLICT DO NOTHING`
- [x] 2.2 Implementar `get_proposicoes_pendentes(limite: int = 50) -> list[Proposicao]` em `camara_repository.py`
      — busca proposições com `classificacao_status = 'pendente_classificacao'` ordenadas por `data_coleta ASC`
- [x] 2.3 Implementar `atualizar_classificacao_status(proposicao_id: int, status: str) -> None` em `camara_repository.py`
- [x] 2.4 Implementar `deletar_proposicao(proposicao_id: int) -> None` em `camara_repository.py`
      — remove proposição (cascata remove tramitacoes, favoritos e proposicao_categoria)

## 3. Redesign do prompt e fluxo Gemini

- [x] 3.1 Substituir `_categorizar_via_gemini(ementa)` por `_classificar_via_gemini(ementa) -> str` em `camara_service.py`
      — novo prompt que retorna "irrelevante" OU nome exato de categoria; lança exceção em falha de API
- [x] 3.2 Adicionar tratamento de `429 ResourceExhausted`: capturar exceção do SDK, aguardar 60s e re-tentar uma vez; se falhar de novo, re-lançar
- [x] 3.3 Substituir `_categorizar_com_fallback(dto)` por `_classificar_e_filtrar(dto) -> tuple[dict, str | None]`
      — retorna `(dto, categoria_nome)` onde `categoria_nome` é None quando Gemini falhou (pendente) ou "irrelevante"
      — define `dto["classificacao_status"]` como `CLASSIFICACAO_PENDENTE` em falha, ou como `CLASSIFICACAO_CLASSIFICADO` quando categorizou
- [x] 3.4 Remover `CATEGORIAS_FIXAS` com "outros" — a nova lista tem 8 categorias sem fallback "outros" (irrelevantes são descartadas)

## 4. Atualização de run_sync()

- [x] 4.1 No início de `run_sync()`, chamar `repo.get_proposicoes_pendentes()` e re-tentar classificação
      — se categoria válida → `vincular_categoria` + `atualizar_classificacao_status('classificado')`
      — se "irrelevante" → `deletar_proposicao`
      — se falha → manter como pendente (será retentada no próximo run)
- [x] 4.2 No loop de ingestão de novas proposições, substituir a chamada ao Gemini antiga pela nova `_classificar_e_filtrar`
      — se categoria_nome == "irrelevante" → `continue` (não adiciona ao lote de upsert)
      — se categoria_nome is None (falha) → adiciona com `classificacao_status = pendente_classificacao`
      — se categoria_nome válida → adiciona ao lote
- [x] 4.3 Após `upsert_proposicoes_lote(dtos)`, iterar sobre dtos que têm categoria e chamar `vincular_categoria` para cada um
- [x] 4.4 Adicionar contador `total_descartados` ao resumo de `run_sync()` e ao `SyncExecution` (campo opcional — logar se não houver coluna)

## 5. Neon — validação de conexão

- [ ] 5.1 Verificar que `DATABASE_URL` no `.env` local e no Neon tem `?sslmode=require`
- [ ] 5.2 Rodar `flask db upgrade` apontando para o Neon (`DATABASE_URL` do Neon no env) para garantir que a migration `ca57241159f9` está aplicada
- [ ] 5.3 Rodar `flask sync-camara` manualmente e confirmar que proposições são inseridas com categorias vinculadas no Neon

## 6. Testes

- [x] 6.1 Testar `seed_categorias()`: verificar que as 8 categorias existem na tabela após a chamada; segunda chamada não duplica
- [x] 6.2 Testar `vincular_categoria()`: inserir proposição e categoria, chamar função, verificar vínculo em `proposicao_categoria`; segunda chamada não duplica
- [x] 6.3 Testar `_classificar_via_gemini` mock com resposta "irrelevante": verificar que proposição não é persistida
- [x] 6.4 Testar `_classificar_via_gemini` mock com categoria válida: verificar que proposição é persistida e vínculo é criado
- [x] 6.5 Testar `_classificar_via_gemini` mock com resposta malformada: verificar `pendente_classificacao` e ausência de vínculo
- [x] 6.6 Testar `_classificar_via_gemini` mock com 429: verificar que aguarda 60s (mock sleep) e re-tenta; na segunda falha, `pendente_classificacao`
- [x] 6.7 Testar retry de pendentes: criar proposição `pendente_classificacao`, rodar `run_sync()` com Gemini mockado retornando categoria → verificar `classificado` e vínculo criado
- [x] 6.8 Testar retry de pendentes com Gemini retornando "irrelevante": verificar que proposição é deletada do banco

## 7. Documentação

- [x] 7.1 Atualizar `docs/db/schema.md` com a tabela `categorias` (seed data) e `proposicao_categoria`
- [x] 7.2 Atualizar `.env.example` se necessário (confirmar que `GEMINI_RATE_LIMIT_RPM` e `DATABASE_URL` estão documentados)
