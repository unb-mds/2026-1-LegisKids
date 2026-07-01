# Referência da API interna

Esta página documenta a API REST exposta pelo backend Flask do LegisKids e
consumida pelo frontend Vue.

!!! info "API interna x API da Câmara"

    Os endpoints desta página pertencem ao próprio LegisKids e usam caminhos
    iniciados por `/api`. A API da Câmara dos Deputados é uma fonte externa,
    consumida pelo backend durante a sincronização, e está descrita no
    [levantamento de APIs](levantamento_api.md).

## URL base

No ambiente local, a API responde em:

```text
http://localhost:5000
```

As respostas usam JSON. Os endpoints documentados nesta página não exigem
autenticação atualmente.

## Resumo dos endpoints

| Método | Endpoint | Finalidade |
|---|---|---|
| `GET` | `/` | Verificar se o serviço Flask está ativo |
| `GET` | `/health` | Verificar a conexão com o banco |
| `GET` | `/api/proposicoes` | Listar e filtrar proposições |
| `GET` | `/api/proposicoes/{id}` | Consultar uma proposição e suas tramitações |
| `GET` | `/api/estatisticas` | Obter dados agregados do dashboard |
| `GET` | `/api/temas` | Listar temas e suas quantidades de proposições |

## Verificar o serviço

### `GET /`

Confirma que o processo Flask está respondendo.

```bash
curl http://localhost:5000/
```

Resposta `200 OK`:

```json
{
  "message": "LegisKids está no ar!",
  "status": "ok"
}
```

## Verificar a conexão com o banco

### `GET /health`

Executa uma conexão simples com o banco configurado na `DATABASE_URL`.

```bash
curl http://localhost:5000/health
```

Resposta `200 OK`:

```json
{
  "database": "conectado",
  "status": "ok"
}
```

Se a conexão falhar, a API retorna `500 Internal Server Error`:

```json
{
  "database": "mensagem retornada pelo driver do banco",
  "status": "erro"
}
```

!!! warning

    O healthcheck confirma a conexão, mas não garante que o schema esteja
    atualizado ou que existam dados cadastrados.

## Listar proposições

### `GET /api/proposicoes`

Retorna proposições ordenadas pela data de apresentação, da mais recente para
a mais antiga. Todos os parâmetros são opcionais e podem ser combinados.

### Parâmetros de consulta

| Parâmetro | Tipo | Padrão | Comportamento |
|---|---|---|---|
| `pagina` | inteiro positivo | `1` | Página solicitada |
| `por_pagina` | inteiro positivo | `10` | Itens por página; valores acima de `50` são limitados a `50` |
| `q` | texto | — | Busca parcial na ementa, sem diferenciar maiúsculas e minúsculas |
| `partido` | texto | — | Busca parcial na sigla do partido, sem diferenciar maiúsculas e minúsculas |
| `data_inicio` | data `AAAA-MM-DD` | — | Data de apresentação mínima, inclusiva |
| `data_fim` | data `AAAA-MM-DD` | — | Data de apresentação máxima, inclusiva |
| `subtema` | texto | — | Busca parcial no nome da categoria vinculada |
| `parlamentar` | texto | — | Reservado; atualmente é aceito, mas não altera o resultado |

Exemplo com filtros e paginação:

```bash
curl "http://localhost:5000/api/proposicoes?q=dados&partido=PT&data_inicio=2024-01-01&subtema=prote%C3%A7%C3%A3o&pagina=1&por_pagina=10"
```

Resposta `200 OK`:

```json
{
  "items": [
    {
      "ano": 2024,
      "categorias": [
        {
          "ativa": true,
          "cor": "#2563EB",
          "descricao": "Proteção de dados pessoais de crianças",
          "icone": "shield",
          "id": 3,
          "nome": "Proteção de dados de menores"
        }
      ],
      "classificacao_status": "classificado",
      "data_apresentacao": "2024-03-15",
      "data_coleta": "2026-06-29T12:00:00",
      "descricao_situacao": "Em tramitação",
      "ementa": "Dispõe sobre a proteção de dados de crianças na internet.",
      "id": 123456,
      "nome_autor": null,
      "numero": 100,
      "partido": {
        "id": 13,
        "nome": "Partido de Exemplo",
        "sigla": "PE"
      },
      "sigla_partido": "PE",
      "sigla_tipo": "PL",
      "status": "Em tramitação",
      "subtema": "Proteção de dados de menores"
    }
  ],
  "pagina": 1,
  "total": 1,
  "total_paginas": 1
}
```

Se não houver resultados, `items` será um array vazio e `total` será `0`.

Parâmetros de paginação inválidos retornam `400 Bad Request`:

```json
{
  "error": "pagina e por_pagina devem ser inteiros positivos"
}
```

Uma falha ao consultar o banco retorna `500 Internal Server Error`:

```json
{
  "error": "Erro ao buscar proposições"
}
```

## Consultar uma proposição

### `GET /api/proposicoes/{id}`

Retorna os dados completos de uma proposição e suas tramitações em ordem
cronológica.

| Parâmetro de rota | Tipo | Descrição |
|---|---|---|
| `id` | inteiro | Identificador oficial da proposição |

```bash
curl http://localhost:5000/api/proposicoes/123456
```

Resposta `200 OK`:

```json
{
  "proposicao": {
    "ano": 2024,
    "categorias": [
      {
        "ativa": true,
        "cor": "#2563EB",
        "descricao": "Proteção de dados pessoais de crianças",
        "icone": "shield",
        "id": 3,
        "nome": "Proteção de dados de menores"
      }
    ],
    "classificacao_status": "classificado",
    "data_apresentacao": "2024-03-15",
    "data_coleta": "2026-06-29T12:00:00",
    "descricao_situacao": "Em tramitação",
    "ementa": "Dispõe sobre a proteção de dados de crianças na internet.",
    "id": 123456,
    "nome_autor": null,
    "numero": 100,
    "partido": {
      "id": 13,
      "nome": "Partido de Exemplo",
      "sigla": "PE"
    },
    "sigla_partido": "PE",
    "sigla_tipo": "PL",
    "status": "Em tramitação",
    "subtema": "Proteção de dados de menores"
  },
  "tramitacoes": [
    {
      "data": "2024-04-01T10:30:00",
      "data_hora": "2024-04-01T10:30:00",
      "descricao": "Recebimento pela comissão",
      "descricao_situacao": "Em tramitação",
      "descricao_tramitacao": "Recebimento pela comissão",
      "id": 987,
      "id_situacao": 100,
      "orgao": "CCJC",
      "proposicao_id": 123456,
      "sigla_orgao": "CCJC"
    }
  ]
}
```

Uma proposição sem tramitações retorna `"tramitacoes": []`.

Se o identificador inteiro não existir, a resposta será `404 Not Found`:

```json
{
  "error": "Proposição não encontrada"
}
```

Uma falha ao consultar o banco retorna `500 Internal Server Error`:

```json
{
  "error": "Erro ao buscar proposição"
}
```

## Consultar estatísticas

### `GET /api/estatisticas`

Retorna os totais utilizados pelos indicadores e gráficos do dashboard.

```bash
curl http://localhost:5000/api/estatisticas
```

Resposta `200 OK`:

```json
{
  "por_status": {
    "labels": [
      "Em tramitação",
      "Arquivado"
    ],
    "values": [
      18,
      4
    ]
  },
  "por_subtema": {
    "labels": [
      "Proteção de dados de menores",
      "Cyberbullying"
    ],
    "values": [
      12,
      10
    ]
  },
  "resumo": {
    "alertas": 0,
    "ativas": 18,
    "subtemas": 2,
    "total": 22
  },
  "temporal": {
    "labels": [
      "Jan/2024",
      "Fev/2024"
    ],
    "values": [
      8,
      14
    ]
  },
  "ultima_atualizacao": "2026-06-29T12:10:00+00:00"
}
```

Quando não há dados, as séries retornam `labels` e `values` vazios. Quando não
há sincronização concluída, `ultima_atualizacao` é `null`. O campo `alertas`
permanece em `0` até a implementação dessa funcionalidade.

Uma falha ao calcular as métricas retorna `500 Internal Server Error`:

```json
{
  "error": "Erro ao calcular estatísticas"
}
```

## Listar temas

### `GET /api/temas`

Retorna todas as categorias, inclusive as que ainda não possuem proposições,
ordenadas pela quantidade de proposições em ordem decrescente.

```bash
curl http://localhost:5000/api/temas
```

Resposta `200 OK`:

```json
[
  {
    "ativa": true,
    "cor": "#2563EB",
    "descricao": "Proteção de dados pessoais de crianças",
    "icone": "shield",
    "id": 3,
    "nome": "Proteção de dados de menores",
    "total": 12
  },
  {
    "ativa": true,
    "cor": "#7C3AED",
    "descricao": "Prevenção e combate ao cyberbullying",
    "icone": "message-circle",
    "id": 1,
    "nome": "Cyberbullying",
    "total": 10
  }
]
```

Se não houver categorias, a resposta será um array vazio. Uma falha ao
consultar o banco retorna `500 Internal Server Error`:

```json
{
  "error": "Erro ao listar temas"
}
```

## Formato geral de erros

As rotas sob `/api` retornam erros em JSON:

```json
{
  "error": "Descrição do erro"
}
```

| Status | Situação |
|---|---|
| `400 Bad Request` | Paginação inválida |
| `404 Not Found` | Proposição ou rota da API não encontrada |
| `500 Internal Server Error` | Falha interna ou de acesso ao banco |

Exemplo para uma rota inexistente:

```bash
curl http://localhost:5000/api/rota-inexistente
```

```json
{
  "error": "Recurso não encontrado"
}
```

## Observações sobre os campos

- Datas usam o padrão ISO 8601.
- `status` é um alias de `descricao_situacao`.
- `subtema` contém o nome da primeira categoria vinculada ou `null`.
- `nome_autor` está reservado e atualmente retorna `null`.
- `data`, `descricao` e `orgao` são aliases usados pelo frontend nas
  tramitações.
- Os exemplos desta página são fictícios e não representam dados ou
  credenciais do ambiente Neon.
