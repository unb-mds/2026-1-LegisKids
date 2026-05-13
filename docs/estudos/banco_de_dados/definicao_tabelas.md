# Definição da Estrutura das Tabelas do Banco de Dados
# Objetivo

Este documento define a estrutura inicial do banco de dados do sistema de análise legislativa sobre segurança da criança na internet.

O objetivo é:

- definir as tabelas principais;
- planejar os relacionamentos;
- garantir integridade dos dados;
- evitar redundância;
- manter baixo custo computacional;
- suportar os dashboards do sistema.

O banco utilizará PostgreSQL e armazenará apenas os dados necessários para análise acadêmica.

# Objetivos da Estrutura

A estrutura do banco deve permitir:

- armazenamento eficiente;
- consultas rápidas;
- baixo uso de armazenamento;
- fácil manutenção;
- expansão futura sem grandes alterações estruturais.

O sistema possui limite aproximado de 200 MB de armazenamento, portanto apenas dados relevantes aos dashboards serão persistidos.

# Entidades Principais

O sistema utilizará as seguintes entidades:

| Entidade | Finalidade |
| --- | --- |
| usuarios | autenticação e preferências |
| proposicoes | proposições legislativas |
| partidos | partidos políticos |
| tramitacoes | andamento legislativo |
| favoritos | proposições salvas pelo usuário |
| historico_consultas | histórico de pesquisas |
| requisicoes_api | monitoramento da coleta |

# Estrutura das Tabelas

## Tabela: usuarios

### Objetivo

Armazenar informações básicas dos usuários do sistema.

### Campos

| Campo | Tipo | Restrições |
| --- | --- | --- |
| id | SERIAL | PRIMARY KEY |
| nome | VARCHAR(100) | NOT NULL |
| email | VARCHAR(150) | UNIQUE NOT NULL |
| google_id | VARCHAR(100) | UNIQUE NOT NULL |
| data_criacao | TIMESTAMP | DEFAULT NOW() |

### Justificativa

Essa tabela permitirá:

- autenticação;
- personalização futura;
- gerenciamento de favoritos;
- histórico de consultas.

# Tabela: partidos

## Objetivo

Armazenar informações simplificadas dos partidos políticos associados às proposições.

## Campos

| Campo | Tipo | Restrições |
| --- | --- | --- |
| id | INTEGER | PRIMARY KEY |
| sigla | VARCHAR(20) | UNIQUE NOT NULL |
| nome | VARCHAR(150) | NOT NULL |

## Origem dos Dados

Endpoint:

```
GET /partidos
```

# Tabela: proposicoes

## Objetivo

Armazenar proposições legislativas relacionadas à segurança da criança na internet.

## Campos

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
| UNIQUE (sigla_tipo, numero, ano) |  | evitar duplicidade lógica |

## Chave Estrangeira

```sql
FOREIGN KEY (partido_id)
REFERENCES partidos(id)
```

## Origem dos Dados

Endpoint:

```
GET /proposicoes
```

## Relacionamento

- um partido pode estar associado a várias proposições;
- uma proposição estará associada a um partido principal.

Relacionamento:

- muitos para um.

## Observação

Para reduzir complexidade e armazenamento, o sistema realizará análises políticas apenas em nível partidário.

Informações individuais de deputados, coautorias e representação regional não serão persistidas no banco de dados.

# Tabela: tramitacoes

## Objetivo

Armazenar histórico simplificado de tramitação legislativa.

## Campos

| Campo | Tipo | Restrições |
| --- | --- | --- |
| id | SERIAL | PRIMARY KEY |
| proposicao_id | INTEGER | NOT NULL FOREIGN KEY |
| data_hora | TIMESTAMP | NOT NULL |
| id_situacao | INTEGER | NOT NULL |
| descricao_situacao | VARCHAR(150) | NOT NULL |
| descricao_tramitacao | TEXT | NOT NULL |
| sigla_orgao | VARCHAR(50) | NOT NULL |

## Chave Estrangeira

```sql
FOREIGN KEY (proposicao_id)
REFERENCES proposicoes(id)
ON DELETE CASCADE
```

## Origem dos Dados

Endpoint:

```
GET /proposicoes/{id}/tramitacoes
```

## Relacionamento

- uma proposição possui várias tramitações.

Relacionamento:

- um para muitos.

# Tabela: favoritos

## Objetivo

Permitir que usuários salvem proposições de interesse.

## Campos

| Campo | Tipo | Restrições |
| --- | --- | --- |
| id | SERIAL | PRIMARY KEY |
| usuario_id | INTEGER | NOT NULL FOREIGN KEY |
| proposicao_id | INTEGER | NOT NULL FOREIGN KEY |
| data_favorito | TIMESTAMP | DEFAULT NOW() |
| UNIQUE (usuario_id, proposicao_id) |  | impedir favoritos duplicados |

## Chaves Estrangeiras

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

## Relacionamento

- um usuário pode favoritar várias proposições;
- uma proposição pode ser favoritada por vários usuários.

Relacionamento:

- muitos para muitos.

# Tabela: historico_consultas

## Objetivo

Armazenar pesquisas realizadas pelos usuários.

## Campos

| Campo | Tipo | Restrições |
| --- | --- | --- |
| id | SERIAL | PRIMARY KEY |
| usuario_id | INTEGER | NOT NULL FOREIGN KEY |
| termo_busca | VARCHAR(255) | NOT NULL |
| data_consulta | TIMESTAMP | DEFAULT NOW() |

## Chave Estrangeira

```sql
FOREIGN KEY (usuario_id)
REFERENCES usuarios(id)
ON DELETE CASCADE
```

## Relacionamento

- um usuário possui várias consultas registradas.

Relacionamento:

- um para muitos.

# Tabela: requisicoes_api

## Objetivo

Registrar execuções de coleta da API.

## Campos

| Campo | Tipo | Restrições |
| --- | --- | --- |
| id | SERIAL | PRIMARY KEY |
| endpoint | VARCHAR(255) | NOT NULL |
| data_requisicao | TIMESTAMP | DEFAULT NOW() |
| quantidade_registros | INTEGER | NOT NULL |
| status_requisicao | VARCHAR(50) | NOT NULL |
| tempo_execucao_ms | INTEGER | monitoramento de desempenho |

## Justificativa

Essa tabela permitirá:

- monitoramento da coleta;
- auditoria simples;
- identificação de falhas;
- controle básico do sistema;
- análise de desempenho da integração com a API.

# Relacionamentos Gerais

## Estrutura Relacional

### Partido → Proposição

- um partido pode estar associado a várias proposições;
- uma proposição estará associada a um partido principal.

Relacionamento:

- um para muitos.

### Proposição → Tramitação

- uma proposição possui várias tramitações.

Relacionamento:

- um para muitos.

### Usuários ↔ Proposições (via favoritos)

- um usuário pode favoritar várias proposições;
- uma proposição pode ser favoritada por vários usuários.

Relacionamento:

- muitos para muitos.

### Usuário → Histórico de Consultas

- um usuário possui várias consultas registradas.

Relacionamento:

- um para muitos.

# Estratégias de Integridade dos Dados

O sistema adotará:

- chaves primárias;
- chaves estrangeiras;
- restrições NOT NULL;
- restrições UNIQUE;
- exclusão em cascata quando necessário;
- uso de IDs oficiais da API da Câmara.

# Estratégias para Evitar Redundância

Para reduzir armazenamento:

- partidos serão separados em tabela própria;
- métricas serão calculadas dinamicamente;
- textos completos das proposições não serão armazenados;
- dados não utilizados pelos dashboards não serão persistidos;
- informações derivadas não serão armazenadas permanentemente;
- informações individuais de parlamentares não serão persistidas.

# Classificação Simplificada de Situação

As situações retornadas pela API serão agrupadas em categorias simplificadas para facilitar análise e visualização.

Exemplos:

- em tramitação;
- arquivado;
- aprovado;
- encerrado;
- outros.

Essa classificação será realizada internamente pelo sistema a partir das descrições retornadas pela API.

# Critério de Coleta das Proposições

As proposições serão coletadas utilizando filtros textuais relacionados ao tema de segurança da criança na internet.

Exemplos de termos:

- criança;
- adolescente;
- internet;
- redes sociais;
- cyberbullying;
- proteção digital;
- segurança online.

Os filtros poderão ser refinados manualmente durante o desenvolvimento do projeto.

# Estrutura Consistente para os Dashboards

| Dashboard | Tabelas Utilizadas |
| --- | --- |
| Panorama Geral | proposicoes |
| Evolução Temporal | proposicoes |
| Análise Política | proposicoes, partidos |
| Tramitação Legislativa | tramitacoes |
| Favoritos do usuário | favoritos |
| Histórico de pesquisa | historico_consultas |

# Justificativa Técnica

A estrutura foi escolhida porque:

- mantém o banco pequeno;
- facilita consultas SQL;
- reduz redundância;
- suporta os dashboards principais;
- facilita manutenção;
- permite futura expansão.

Além disso:

- PostgreSQL lida facilmente com esse volume de dados;
- o sistema não necessita arquitetura distribuída;
- não há necessidade de Big Data ou processamento complexo.

# Conclusão

A estrutura definida atende aos objetivos acadêmicos e técnicos do sistema.

As tabelas propostas permitem:

- análise legislativa;
- análise política partidária;
- monitoramento temporal;
- acompanhamento de tramitação;
- gerenciamento de usuários;
- favoritos;
- histórico de consultas;
- controle básico da coleta da API.

O modelo relacional mantém:

- integridade dos dados;
- simplicidade;
- baixo consumo de armazenamento;
- facilidade de manutenção;
- possibilidade de expansão futura.