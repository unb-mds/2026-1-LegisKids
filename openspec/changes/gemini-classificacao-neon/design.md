# Design — gemini-classificacao-neon

## Visão geral do fluxo redesenhado

```
Scheduler (APScheduler)
       │
       ▼
CamaraService.run_sync()
       │
       ├─ [1] buscar página da API da Câmara (paginação, retry)
       │
       ├─ [2] filtrar por palavras-chave (pré-filtro barato, já existente)
       │
       ├─ [3] validar + normalizar (já existente)
       │
       ├─ [4] classificar via Gemini  ◀── REDESENHADO
       │         │
       │         ├─ retorna "irrelevante" → DESCARTAR (não persiste)
       │         ├─ retorna categoria válida → dto["categoria_nome"] = categoria
       │         └─ falha/timeout → dto["classificacao_status"] = pendente
       │
       ├─ [5] upsert_proposicoes_lote(dtos relevantes)  (já existente)
       │
       └─ [6] vincular_categoria(proposicao_id, categoria_nome) ◀── NOVO
                  INSERT INTO proposicao_categoria ON CONFLICT DO NOTHING
```

## 1. Redesign do prompt Gemini

### Decisão: uma chamada, duas perguntas

Uma única chamada decide relevância e categoria. Isso economiza RPM e mantém o rate limit simples.

**Prompt:**
```
Você é um classificador de proposições legislativas brasileiras.

Analise a ementa abaixo e responda com UMA das seguintes opções:
- "irrelevante" → se NÃO tratar de proteção de crianças ou adolescentes no ambiente digital/internet
- Um dos temas abaixo → se a proposta tratar do tema

Temas válidos:
- cyberbullying
- exploração sexual infantil online
- proteção de dados de menores
- segurança digital infantil
- regulação de plataformas digitais
- conteúdos nocivos para menores
- crimes virtuais contra crianças
- privacidade de menores

Responda SOMENTE com a palavra ou frase exata. Sem explicação.

Ementa: {ementa[:600]}
```

**Parsing da resposta:**
- strip + lower
- Se `== "irrelevante"` → descartar
- Se `in CATEGORIAS_FIXAS` → vincular
- Qualquer outra resposta → `pendente_classificacao` (resposta malformada)

### Rate limiting (mantido)

```python
min_interval = 60.0 / RPM   # 4s para 15 RPM
sleep(max(0, min_interval - elapsed))
```

Adição: capturar `429 ResourceExhausted` do SDK do Gemini e aguardar 60s antes de re-tentar (uma vez).

### Limite diário (1500 RPD)

O scheduler roda de hora em hora. Cada run processa no máximo `N` proposições via Gemini. Com 15 RPM e 1h de intervalo, o pior caso é 15 × 60 = 900 chamadas por run — dentro dos 1500 RPD se houver só 1 run pesado por dia. Não implementar contador de RPD agora; o fallback para `pendente_classificacao` absorve o overflow naturalmente.

## 2. Seed de categorias

Função `seed_categorias()` no `camara_repository.py`:

```python
SEED_CATEGORIAS = [
    {"nome": "cyberbullying",                     "cor": "#EF4444", "icone": "shield-alert"},
    {"nome": "exploração sexual infantil online", "cor": "#DC2626", "icone": "alert-triangle"},
    {"nome": "proteção de dados de menores",      "cor": "#3B82F6", "icone": "lock"},
    {"nome": "segurança digital infantil",        "cor": "#8B5CF6", "icone": "shield"},
    {"nome": "regulação de plataformas digitais", "cor": "#F59E0B", "icone": "globe"},
    {"nome": "conteúdos nocivos para menores",    "cor": "#EC4899", "icone": "eye-off"},
    {"nome": "crimes virtuais contra crianças",   "cor": "#6366F1", "icone": "gavel"},
    {"nome": "privacidade de menores",            "cor": "#10B981", "icone": "user-shield"},
]
```

Inserção idempotente via:
```sql
INSERT INTO categorias (nome, descricao, cor, icone, ativa)
VALUES (%s, %s, %s, %s, true)
ON CONFLICT (nome) DO NOTHING
```

Chamada em `app.py` dentro do `app_context()` após `db.init_app(app)`.

## 3. Vinculação proposicao → categoria

Nova função `vincular_categoria(proposicao_id, categoria_nome)` em `camara_repository.py`:

1. Busca `categoria_id` pelo nome (lookup simples, categorias são poucas e fixas — pode usar cache em memória)
2. Insere em `proposicao_categoria` com `ON CONFLICT DO NOTHING`

Cache de categorias em memória (dict `nome → id`) para evitar N queries de lookup:

```python
_cache_categorias: dict[str, int] = {}

def _get_categoria_id(nome: str) -> int | None:
    if nome not in _cache_categorias:
        cat = db.session.query(Categoria.id).filter_by(nome=nome).scalar()
        if cat:
            _cache_categorias[nome] = cat
    return _cache_categorias.get(nome)
```

## 4. Integração no service

Mudanças em `run_sync()`:

```python
# Antes (atual — categoria se perde):
dto = self._categorizar_com_fallback(dto)
dtos.append(dto)

# Depois — categoria retorna junto:
dto, categoria_nome = self._classificar_e_filtrar(dto)
if categoria_nome is None and dto["classificacao_status"] == IRRELEVANTE:
    continue  # descartar
dtos.append((dto, categoria_nome))

# Após upsert:
for dto, categoria_nome in dtos_com_categoria:
    if categoria_nome:
        repo.vincular_categoria(dto["id"], categoria_nome)
```

## 5. Retry de pendentes

No início de `run_sync()`, antes de buscar novas proposições:

```python
pendentes = repo.get_proposicoes_pendentes(limite=50)
for prop in pendentes:
    dto, categoria_nome = self._classificar_e_filtrar({"id": prop.id, "ementa": prop.ementa, ...})
    if categoria_nome:
        repo.vincular_categoria(prop.id, categoria_nome)
        repo.atualizar_classificacao_status(prop.id, CLASSIFICACAO_CLASSIFICADO)
    elif dto["classificacao_status"] == "irrelevante":
        repo.deletar_proposicao(prop.id)  # era pendente, agora sabemos: irrelevante
```

## 6. Neon — sslmode

Sem mudança de código. Apenas garantir que `.env` / variável de ambiente tenha:
```
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require
```

SQLAlchemy passa o parâmetro automaticamente via query string.

## Invariantes

- Toda proposição no banco tem `classificacao_status = 'classificado'` OU `'pendente_classificacao'`
- Toda proposição com `classificacao_status = 'classificado'` tem ao menos um vínculo em `proposicao_categoria`
- `seed_categorias()` é idempotente — pode rodar múltiplas vezes sem duplicar
- `vincular_categoria()` é idempotente — `ON CONFLICT DO NOTHING` garante
- Proposições irrelevantes nunca chegam ao banco
