# Detalhamento das Tabelas do Banco de Dados

# Objetivo

Foram definidos os campos, tipos de dados e relacionamentos das tabelas principais do sistema de análise legislativa sobre segurança da criança na internet.

A modelagem foi construída considerando:

- simplicidade;
- baixo consumo de armazenamento;
- compatibilidade com PostgreSQL;
- aderência aos dashboards definidos;
- integração com a API da Câmara dos Deputados.

# Tabelas Definidas

## 1. usuarios

### Objetivo

Armazenar informações básicas dos usuários autenticados no sistema.

| Campo | Tipo | Restrições |
| --- | --- | --- |
| id | SERIAL | PRIMARY KEY |
| nome | VARCHAR(100) | NOT NULL |
| email | VARCHAR(150) | UNIQUE NOT NULL |
| google_id | VARCHAR(100) | UNIQUE NOT NULL |
| data_criacao | TIMESTAMP | DEFAULT NOW() |

## 2. partidos

### Objetivo

Armazenar informações simplificadas dos partidos políticos associados às proposições.

| Campo | Tipo | Restrições |
| --- | --- | --- |
| id | INTEGER | PRIMARY KEY |
| sigla | VARCHAR(20) | UNIQUE NOT NULL |
| nome | VARCHAR(150) | NOT NULL |

### Origem dos Dados

```
GET /partidos
```

## 3. proposicoes

### Objetivo

Armazenar proposições legislativas relacionadas ao tema do projeto.

| Campo | Tipo | Restrições |
| --- | --- | --- |
| id | INTEGER | PRIMARY KEY |
| sigla_tipo | VARCHAR(20) | NOT NULL |
| numero | INTEGER | NOT NULL |
| ano | INTEGER | NOT NULL |
| ementa | TEXT | NOT NULL |
| data_apresentacao | DATE | NOT NULL |
| descricao_situacao | VARCHAR(150) | NOT NULL |
| partido_id | INTEGER | FOREIGN KEY |
| sigla_partido | VARCHAR(20) | NOT NULL |
| data_coleta | TIMESTAMP | DEFAULT NOW() |

### Restrições Adicionais

```sql
UNIQUE (sigla_tipo, numero, ano)
```

### Chave Estrangeira

```sql
FOREIGN KEY (partido_id)
REFERENCES partidos(id)
```

### Origem dos Dados

```
GET /proposicoes
```

### Observação

A análise política será realizada apenas em nível partidário para reduzir complexidade e armazenamento.

Informações individuais de deputados e coautorias não serão persistidas.

## 4. tramitacoes

### Objetivo

Armazenar histórico simplificado de tramitação legislativa.

| Campo | Tipo | Restrições |
| --- | --- | --- |
| id | SERIAL | PRIMARY KEY |
| proposicao_id | INTEGER | NOT NULL FOREIGN KEY |
| data_hora | TIMESTAMP | NOT NULL |
| id_situacao | INTEGER | NOT NULL |
| descricao_situacao | VARCHAR(150) | NOT NULL |
| descricao_tramitacao | TEXT | NOT NULL |
| sigla_orgao | VARCHAR(50) | NOT NULL |

### Chave Estrangeira

```sql
FOREIGN KEY (proposicao_id)
REFERENCES proposicoes(id)
ON DELETE CASCADE
```

### Origem dos Dados

```
GET /proposicoes/{id}/tramitacoes
```

## 5. favoritos

### Objetivo

Permitir que usuários salvem proposições de interesse.

| Campo | Tipo | Restrições |
| --- | --- | --- |
| id | SERIAL | PRIMARY KEY |
| usuario_id | INTEGER | NOT NULL FOREIGN KEY |
| proposicao_id | INTEGER | NOT NULL FOREIGN KEY |
| data_favorito | TIMESTAMP | DEFAULT NOW() |

### Restrição Adicional

```sql
UNIQUE (usuario_id, proposicao_id)
```

### Chaves Estrangeiras

```sql
FOREIGN KEY (usuario_id)
REFERENCES usuarios(id)
ON DELETE CASCADE
```

```sql
FOREIGN KEY (proposicao_id)
REFERENCES proposicoes(id)
ON DELETE CASCADE
```

## 6. historico_consultas

### Objetivo

Armazenar pesquisas realizadas pelos usuários.

| Campo | Tipo | Restrições |
| --- | --- | --- |
| id | SERIAL | PRIMARY KEY |
| usuario_id | INTEGER | NOT NULL FOREIGN KEY |
| termo_busca | VARCHAR(255) | NOT NULL |
| data_consulta | TIMESTAMP | DEFAULT NOW() |

### Chave Estrangeira

```sql
FOREIGN KEY (usuario_id)
REFERENCES usuarios(id)
ON DELETE CASCADE
```

## 7. requisicoes_api

### Objetivo

Registrar execuções de coleta da API.

| Campo | Tipo | Restrições |
| --- | --- | --- |
| id | SERIAL | PRIMARY KEY |
| endpoint | VARCHAR(255) | NOT NULL |
| data_requisicao | TIMESTAMP | DEFAULT NOW() |
| quantidade_registros | INTEGER | NOT NULL |
| status_requisicao | VARCHAR(50) | NOT NULL |
| tempo_execucao_ms | INTEGER | NULL |

# Estratégias de Padronização

O banco seguirá os seguintes padrões:

- nomes de tabelas em minúsculo;
- uso de `snake_case`;
- IDs numéricos inteiros;
- timestamps utilizando `TIMESTAMP`;
- textos curtos utilizando `VARCHAR`;
- textos longos utilizando `TEXT`;
- uso de chaves estrangeiras para integridade relacional.

# Estratégias de Integridade

Serão utilizados:

- `PRIMARY KEY`;
- `FOREIGN KEY`;
- `UNIQUE`;
- `NOT NULL`;
- `ON DELETE CASCADE` quando necessário.

# Compatibilidade com os Dashboards