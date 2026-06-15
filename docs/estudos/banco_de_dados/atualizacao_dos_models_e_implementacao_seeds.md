# Atualização dos Models

## Objetivo

Este documento registra as alterações realizadas na modelagem do banco de dados do projeto LegisKids.

As modificações tiveram como objetivo:

- adequar o banco aos requisitos dos dashboards;
- melhorar a normalização dos dados;
- permitir análises por categoria temática;
- manter a estrutura simples e sem entidades desnecessárias.

---

## Alterações Realizadas nos Models

### Inclusão da Entidade Categoria

Foi criada a tabela `categorias` para armazenar classificações temáticas das proposições.

#### Campos

| Campo | Tipo | Restrições |
| --- | --- | --- |
| id | Integer | PRIMARY KEY |
| nome | String(100) | NOT NULL, UNIQUE |
| descricao | Text | opcional |
| cor | String(7) | opcional |
| icone | String(50) | opcional |
| ativa | Boolean | DEFAULT True |

Exemplos de categorias:

- Cyberbullying
- Redes Sociais
- Proteção Digital
- Criança e Adolescente

---

### Inclusão da Tabela Associativa Proposição-Categoria

Foi implementada uma relação muitos-para-muitos entre proposições e categorias.

Tabela:

```text
proposicao_categoria
```

Campos:

| Campo | Tipo |
| --- | --- |
| proposicao_id | Integer (FK) |
| categoria_id | Integer (FK) |

Relacionamento:

```text
Proposição (N) ──────── (N) Categoria
```

Uma proposição pode pertencer a várias categorias. Uma categoria pode classificar várias proposições.

---

### Estrutura Atual de Proposições

A tabela `proposicoes` mantém os seguintes relacionamentos:

```text
Partido (1) ──────── (N) Proposição
Proposição (N) ────── (N) Categoria
Proposição (1) ────── (N) Tramitação
Usuário (1) ─────── (N) Favorito
```

---

## Índices Criados

Foram adicionados índices para melhorar consultas utilizadas pelos dashboards.

| Índice | Coluna(s) |
| --- | --- |
| `idx_proposicoes_sigla_tipo` | `sigla_tipo` |
| `idx_proposicoes_descricao_situacao` | `descricao_situacao` |
| `idx_proposicoes_data_apresentacao` | `data_apresentacao` |
| `idx_proposicoes_partido_id` | `partido_id` |
| `idx_proposicoes_categoria` | `categoria` |
| `idx_proposicoes_ano` | `ano` |
| `idx_proposicoes_tipo_ano` | `sigla_tipo`, `ano` |
| `idx_favoritos_usuario_proposicao` | `usuario_id`, `proposicao_id` |

Benefícios:

- consultas mais rápidas;
- melhor desempenho dos gráficos;
- menor tempo de resposta da API.

---

## Migração do Banco

Após a atualização dos models foram geradas migrations utilizando:

```bash
flask db migrate -m "add autores e categorias"
flask db migrate -m "add constraints and indexes"
flask db migrate -m "remove autores"
```

Posteriormente as migrations foram aplicadas:

```bash
flask db upgrade
```

---

## Situação Atual

O banco de dados possui as seguintes entidades:

```text
usuarios
partidos
categorias
proposicoes
proposicao_categoria
tramitacoes
favoritos
historico_consultas
requisicoes_api
```

Todos os relacionamentos estão implementados e as migrations foram aplicadas com sucesso.