# Tratamento de Dados Antes da Persistência
## Objetivo

Este documento define como os dados recebidos pelo sistema serão tratados antes de serem armazenados no banco de dados.

O objetivo é garantir:

- integridade;
- padronização;
- segurança;
- consistência;
- confiabilidade dos dados.

As regras aqui descritas serão aplicadas tanto aos dados vindos da API da Câmara quanto aos dados inseridos por usuários no sistema.

# Fluxo de Tratamento dos Dados

Todos os dados seguirão o seguinte fluxo antes da persistência:

```
Recebimento dos Dados
        ↓
Validação
        ↓
Sanitização
        ↓
Normalização
        ↓
Transformações Necessárias
        ↓
Persistência no Banco
```

# Estratégias de Validação

## Objetivo

Garantir que apenas dados válidos sejam armazenados no sistema.

## Regras Gerais de Validação

### Campos Obrigatórios

Campos marcados como obrigatórios deverão:

- existir no payload;
- não ser nulos;
- não estar vazios.

| Campo | Regra |
| --- | --- |
| email | obrigatório |
| nome | obrigatório |
| id | obrigatório |
| ementa | obrigatório |

## Validação de Tipos

Cada campo deverá respeitar o tipo esperado definido na modelagem.

| Tipo | Validação |
| --- | --- |
| INTEGER | apenas números inteiros |
| VARCHAR | texto curto |
| TEXT | texto longo |
| DATE | formato de data válido |
| TIMESTAMP | data e hora válidas |

## Validação de Formatos

### Emails

Os emails deverão:

- possuir formato válido;
- conter `@`;
- conter domínio válido.

Exemplo:

```
usuario@email.com
```

### Datas

As datas serão convertidas para o padrão ISO.

```
YYYY-MM-DD
```

Exemplo:

```
2026-05-19
```

### IDs

IDs externos recebidos da API deverão:

- ser numéricos;
- possuir valor positivo;
- não conter caracteres especiais.

# Estratégias de Normalização

## Objetivo

Padronizar os dados armazenados para facilitar:

- buscas;
- filtros;
- análises;
- comparações;
- dashboards.

## Regras de Normalização

### Remoção de Espaços Extras

Será aplicado:

```
trim()
```

Exemplo:

```
"  Projeto de Lei  "
↓
"Projeto de Lei"
```

### Conversão de Texto

| Tipo de Dado | Estratégia |
| --- | --- |
| emails | lowercase |
| siglas partidárias | uppercase |
| textos descritivos | preservados |

Exemplos:

```
USUARIO@EMAIL.COM
↓
usuario@email.com
```

```
pt
↓
PT
```

### Padronização de Datas

Todas as datas serão armazenadas em formato PostgreSQL compatível.

| Tipo | Formato |
| --- | --- |
| DATE | YYYY-MM-DD |
| TIMESTAMP | YYYY-MM-DD HH:MM:SS |

### Padronização de Valores Vazios

| Situação | Tratamento |
| --- | --- |
| string vazia | NULL |
| campo ausente | NULL |
| espaços em branco | NULL |

# Estratégias de Sanitização

## Objetivo

Evitar vulnerabilidades e armazenamento de dados inseguros.

## Proteções Aplicadas

### SQL Injection

O sistema utilizará:

- queries parametrizadas;
- ORM ou query builder;
- prepared statements.

Nunca serão utilizadas concatenações diretas em SQL.

### Sanitização de Strings

Caracteres perigosos serão tratados antes da persistência.

Exemplos:

- remoção de scripts;
- escape de caracteres especiais;
- bloqueio de HTML malicioso.

### Limitação de Tamanho

| Campo | Limite |
| --- | --- |
| nome | 100 caracteres |
| email | 150 caracteres |
| sigla | 20 caracteres |

### Controle de Inputs

O sistema rejeitará:

- tipos inválidos;
- payloads malformados;
- campos inesperados;
- dados incompatíveis com a modelagem.

# Estratégias de Transformação

## Objetivo

Adequar os dados ao padrão interno do sistema antes da persistência.

## Transformações Definidas

### Conversão de Datas da API

```
19/05/2026
↓
2026-05-19
```

### Conversão de Campos Numéricos

```
"123"
↓
123
```

### Extração de Dados Relevantes

Apenas informações necessárias ao sistema serão persistidas.

Exemplos:

- proposições relevantes;
- partido principal;
- tramitações importantes.

Dados redundantes serão descartados.

### Padronização de Status

| Valor Externo | Valor Interno |
| --- | --- |
| Em tramitação | EM_TRAMITACAO |
| Arquivada | ARQUIVADA |

# Tratamentos Adicionais de Dados

## Tratamento de Valores Nulos

| Situação | Tratamento |
| --- | --- |
| campo opcional ausente | NULL |
| campo obrigatório ausente | rejeição da requisição |
| valor inválido | descarte ou erro |
| texto vazio | NULL |

## Tratamento de Caracteres Especiais

### Estratégias

- utilização de UTF-8;
- remoção de caracteres invisíveis;
- normalização de acentuação quando necessário;
- escape de caracteres especiais.

Exemplo:

```
" João Silva "
↓
"João Silva"
```

## Tratamento de Dados Duplicados

### Estratégias

- utilização de `UNIQUE`;
- verificação prévia antes da inserção;
- atualização de registros existentes;
- descarte de duplicidades da API.

Exemplo:

```sql
UNIQUE (sigla_tipo, numero, ano)
```

## Tratamento de Logs e Auditoria

### Registro de:

- erros de validação;
- falhas de integração;
- requisições realizadas;
- horários de coleta;
- quantidade de registros processados.

## Tratamento de Dados Sensíveis

### Estratégias

- não armazenamento de senhas;
- autenticação via Google OAuth;
- armazenamento mínimo de dados pessoais;
- proteção de tokens de autenticação.

## Tratamento de Dados Vindos da API

### Estratégias

- validação de payloads recebidos;
- tolerância a campos ausentes;
- fallback para valores inconsistentes;
- controle de versionamento da API;
- tratamento de timeout e falhas de conexão.

## Tratamento de Erros

| Tipo de Erro | Ação |
| --- | --- |
| dado inválido | rejeitar |
| falha de conexão | retry |
| timeout | registrar log |
| erro inesperado | rollback |

## Estratégias de Transações

### Objetivo

Garantir integridade durante operações múltiplas.

### Estratégias

Utilização de transações para:

- inserções em múltiplas tabelas;
- atualizações encadeadas;
- persistência de tramitações;
- sincronização de dados da API.

Exemplo:

```sql
BEGIN;
INSERT ...
UPDATE ...
COMMIT;
```

## Estratégias de Performance

### Estratégias

- indexação de campos de busca;
- paginação de consultas;
- limitação de payloads;
- armazenamento apenas de dados relevantes.

## Estratégias de Versionamento de Dados

### Estratégias

- migrations controladas;
- versionamento do schema;
- compatibilidade entre versões;
- histórico de alterações estruturais.

# Garantia de Consistência

## Estratégias Utilizadas

O sistema utilizará:

- validação antes da persistência;
- restrições no banco;
- chaves estrangeiras;
- campos obrigatórios;
- normalização de formatos;
- controle de duplicidade.

## Controle de Duplicidade

```sql
UNIQUE (sigla_tipo, numero, ano)
```

```sql
UNIQUE (usuario_id, proposicao_id)
```

# Compatibilidade com PostgreSQL

As estratégias foram planejadas considerando:

- compatibilidade com PostgreSQL;
- uso eficiente de armazenamento;
- integridade relacional;
- facilidade de manutenção;
- performance de consultas.

# Boas Práticas Aplicadas

## Segurança

- prevenção contra SQL Injection;
- sanitização de entradas;
- validação de payloads;
- prepared statements.

## Padronização

- uso de snake_case;
- formatos únicos de data;
- normalização textual;
- padronização de status.

## Qualidade dos Dados

- remoção de inconsistências;
- validação de obrigatoriedade;
- prevenção de duplicidade;
- tratamento de valores inválidos.