# Otimização do Banco de Dados: Índices e Constraints

## Objetivo

Este documento registra as otimizações aplicadas ao banco de dados do sistema LegisKids, com foco em desempenho de consultas e integridade dos dados.

As alterações foram realizadas por meio de uma migration Alembic e validadas diretamente no banco PostgreSQL.

## Motivação

Com o crescimento do volume de proposições coletadas da API da Câmara dos Deputados, as consultas realizadas pelos dashboards passaram a demandar índices específicos para garantir tempo de resposta adequado.

Além disso, a ausência de constraints de unicidade permitia a inserção de registros duplicados, comprometendo a consistência dos dados armazenados.

## Alterações Realizadas

### Índices Adicionados em `proposicoes`

| Índice | Coluna(s) | Justificativa |
| --- | --- | --- |
| `idx_proposicoes_sigla_tipo` | `sigla_tipo` | filtro por tipo de proposição nos dashboards |
| `idx_proposicoes_descricao_situacao` | `descricao_situacao` | filtro por status legislativo |
| `idx_proposicoes_data_apresentacao` | `data_apresentacao` | ordenação e filtro temporal |
| `idx_proposicoes_partido_id` | `partido_id` | join com tabela de partidos |
| `idx_proposicoes_autor_id` | `autor_id` | join com tabela de autores |
| `idx_proposicoes_categoria` | `categoria` | filtro por categoria temática |
| `idx_proposicoes_ano` | `ano` | agrupamento por ano |
| `idx_proposicoes_tipo_ano` | `sigla_tipo`, `ano` | índice composto para consultas combinadas |

### Índice Adicionado em `favoritos`

| Índice | Coluna(s) | Justificativa |
| --- | --- | --- |
| `idx_favoritos_usuario_proposicao` | `usuario_id`, `proposicao_id` | otimiza consulta de favoritos por usuário |

### Constraints de Unicidade

| Constraint | Tabela | Coluna(s) | Justificativa |
| --- | --- | --- | --- |
| `uq_proposicoes_url_api` | `proposicoes` | `url_api` | evita duplicatas de proposições coletadas da API |
| `uq_favorito_usuario_proposicao` | `favoritos` | `usuario_id`, `proposicao_id` | impede que um usuário favorite a mesma proposição duas vezes |
| `uq_autores_email` | `autores` | `email` | garante unicidade de email por autor |

### CHECK Constraint

| Constraint | Tabela | Coluna | Valores Permitidos |
| --- | --- | --- | --- |
| `ck_proposicao_status` | `proposicoes` | `descricao_situacao` | `Em tramitação`, `Aprovado`, `Arquivado`, `Encerrado` |

A constraint foi definida no model SQLAlchemy dentro de `__table_args__`.

### Coluna Adicionada em `proposicoes`

| Coluna | Tipo | Restrições | Justificativa |
| --- | --- | --- | --- |
| `url_api` | `VARCHAR(255)` | `NOT NULL`, `UNIQUE` | armazena a URL oficial da proposição na API da Câmara, evitando recoletas desnecessárias |

## Migration Gerada

```
Revision ID : 45778e94407e
Revises     : a09e20d36ab9
Descrição   : add constraints and indexes
```

A migration foi aplicada com sucesso via `flask db upgrade`.

### Estratégia Adotada para `url_api`

Como a tabela `proposicoes` já continha registros, a coluna foi adicionada em três etapas dentro da migration para evitar violação de `NOT NULL`:

1. coluna adicionada como `nullable=True`;
2. linhas existentes preenchidas com URL derivada do `id` da proposição;
3. coluna alterada para `nullable=False` e constraint `UNIQUE` aplicada.

## Validação

### Teste de Unicidade — `usuarios.email`

Tentativa de inserir dois usuários com o mesmo email retornou:

```
UniqueViolation: duplicar valor da chave viola a restrição de unicidade "usuarios_email_key"
```

### Teste de Unicidade — `proposicoes.url_api`

Tentativa de atribuir a mesma URL a duas proposições distintas retornou:

```
UniqueViolation: duplicar valor da chave viola a restrição de unicidade "uq_proposicoes_url_api"
```

### Índices Confirmados no Banco

Consulta executada:

```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'proposicoes'
ORDER BY indexname;
```

Resultado:

| indexname | descrição |
| --- | --- |
| `idx_proposicoes_ano` | índice em `ano` |
| `idx_proposicoes_autor_id` | índice em `autor_id` |
| `idx_proposicoes_categoria` | índice em `categoria` |
| `idx_proposicoes_data_apresentacao` | índice em `data_apresentacao` |
| `idx_proposicoes_descricao_situacao` | índice em `descricao_situacao` |
| `idx_proposicoes_partido_id` | índice em `partido_id` |
| `idx_proposicoes_sigla_tipo` | índice em `sigla_tipo` |
| `idx_proposicoes_tipo_ano` | índice composto em `sigla_tipo`, `ano` |
| `proposicoes_pkey` | chave primária em `id` |
| `proposicoes_sigla_tipo_numero_ano_key` | unicidade em `sigla_tipo`, `numero`, `ano` |
| `uq_proposicoes_url_api` | unicidade em `url_api` |

## Impacto Esperado

| Consulta | Benefício |
| --- | --- |
| listagem por tipo de proposição | índice em `sigla_tipo` elimina varredura completa |
| filtro por status legislativo | índice em `descricao_situacao` |
| ordenação por data | índice em `data_apresentacao` |
| join com autores | índice em `autor_id` |
| join com partidos | índice em `partido_id` |
| consulta de favoritos por usuário | índice composto elimina varredura na tabela |
| coleta incremental da API | constraint `UNIQUE` em `url_api` impede reinsercão |

## Conclusão

As otimizações aplicadas garantem:

- integridade dos dados por meio de constraints de unicidade e CHECK;
- desempenho adequado nas consultas dos dashboards por meio dos índices criados;
- consistência na coleta incremental de dados da API da Câmara;
- migration versionada e reversível via Alembic.