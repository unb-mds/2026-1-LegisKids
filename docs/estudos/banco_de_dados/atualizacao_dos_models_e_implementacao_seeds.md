# Atualização dos Models e Implementação das Seeds

# Objetivo

Este documento registra as alterações realizadas na modelagem do banco de dados e na criação dos dados iniciais (seed) do projeto LegisKids.

As modificações tiveram como objetivo:

- adequar o banco aos requisitos dos dashboards;
- melhorar a normalização dos dados;
- permitir análises por autor e categoria;
- facilitar testes do sistema durante o desenvolvimento;
- disponibilizar uma base inicial consistente para frontend e backend.

---

# Alterações Realizadas nos Models

## Inclusão da Entidade Autor

Foi criada a tabela `autores` para armazenar os parlamentares responsáveis pelas proposições.

### Campos

| Campo | Tipo |
|---------|---------|
| id | Integer |
| nome | String |

### Relacionamento

```text
Autor (1) ──────── (N) Proposição
```

Um autor pode possuir várias proposições.

Cada proposição possui um único autor principal.

---

## Inclusão da Entidade Categoria

Foi criada a tabela `categorias` para armazenar classificações temáticas das proposições.

### Campos

| Campo | Tipo |
|---------|---------|
| id | Integer |
| nome | String |

Exemplos:

- Cyberbullying
- Redes Sociais
- Proteção Digital
- Criança e Adolescente

---

## Inclusão da Tabela Associativa Proposição-Categoria

Foi implementada uma relação muitos-para-muitos entre proposições e categorias.

Tabela:

```text
proposicao_categoria
```

Campos:

| Campo | Tipo |
|---------|---------|
| proposicao_id | Integer |
| categoria_id | Integer |

Relacionamento:

```text
Proposição (N) ──────── (N) Categoria
```

Uma proposição pode pertencer a várias categorias.

Uma categoria pode classificar várias proposições.

---

## Alteração da Tabela Proposições

Foi adicionada a chave estrangeira:

```python
autor_id
```

Relacionamento:

```python
autor = db.relationship(...)
```

Estrutura atual:

```text
Partido (1) ──────── (N) Proposição
Autor   (1) ──────── (N) Proposição
```

---

## Índices Criados

Foram adicionados índices para melhorar consultas utilizadas pelos dashboards.

### Índices

```python
idx_proposicoes_ano
idx_proposicoes_categoria
idx_proposicoes_data_apresentacao
idx_proposicoes_descricao_situacao
idx_proposicoes_partido_id
idx_proposicoes_sigla_tipo
idx_proposicoes_tipo_ano
```

Benefícios:

- consultas mais rápidas;
- melhor desempenho dos gráficos;
- menor tempo de resposta da API.

---

# Migração do Banco

Após a atualização dos models foi gerada uma migration utilizando:

```bash
flask db migrate -m "add autores e categorias"
```

O Alembic detectou automaticamente:

- criação da tabela `autores`;
- criação da tabela `categorias`;
- criação da tabela `proposicao_categoria`;
- inclusão da coluna `autor_id`;
- criação dos índices;
- criação da chave estrangeira para autores.

Posteriormente a migration foi aplicada:

```bash
flask db upgrade
```

Resultado:

```text
Upgrade executado com sucesso.
```

---

# Implementação do Seed

Foi criado o arquivo:

```text
scripts/seed.py
```

Responsável por popular o banco com dados iniciais para desenvolvimento.

---

# Dados Inseridos

## Partidos

Foram cadastrados partidos utilizados nas proposições de teste.

Exemplos:

- PT
- PL
- MDB
- PSD
- União Brasil
- PP
- PSB

---

## Categorias

Foram cadastradas categorias temáticas.

Exemplos:

- Cyberbullying
- Redes Sociais
- Proteção Digital
- Criança e Adolescente

---

## Autores

Foram cadastrados autores fictícios para simular parlamentares.

Exemplos:

```text
Ana Silva
Carlos Souza
Mariana Lima
João Ferreira
Pedro Almeida
```

---

## Proposições

Foram inseridas proposições de exemplo contendo:

- tipo;
- número;
- ano;
- ementa;
- situação;
- partido;
- autor;
- categorias.

Esses registros permitem:

- testar filtros;
- testar dashboards;
- validar relacionamentos;
- demonstrar funcionamento do sistema.

---

# Problemas Encontrados Durante a Implementação

## Erro de DATABASE_URL

Durante a geração da migration ocorreu:

```text
RuntimeError: DATABASE_URL não configurada no ambiente
```

Solução:

Foi adicionada a variável:

```env
DATABASE_URL=postgresql://postgres:@localhost:5432/legiskids
```

no arquivo `.env`.

---

## Erro de Chave Duplicada

Durante a execução do seed ocorreu:

```text
duplicate key value violates unique constraint
```

Motivo:

Já existiam partidos cadastrados no banco.

Exemplo:

```text
PT
PL
MDB
```

A solução foi alterar o seed para verificar a existência dos registros antes de inserir novos dados.

---

# Resultado da Execução do Seed

Execução:

```bash
python scripts/seed.py
```

Resultado:

```text
✓ Partidos: 7 inseridos
✓ Categorias: 4 inseridas
✓ Autores: 10 inseridos
✓ Proposições: 20 inseridas

Seed concluída.
```

---

# Benefícios Obtidos

As alterações trouxeram diversas melhorias:

- modelagem mais próxima da realidade legislativa;
- suporte a análises por autor;
- suporte a análises por categoria;
- melhor organização dos dados;
- maior normalização do banco;
- facilidade para testes do frontend;
- facilidade para demonstrações do projeto;
- melhor suporte aos dashboards previstos.

---

# Situação Atual

O banco de dados agora possui as seguintes entidades:

```text
usuarios
partidos
autores
categorias
proposicoes
proposicao_categoria
tramitacoes
favoritos
historico_consultas
requisicoes_api
```

Todos os relacionamentos estão implementados, as migrations foram aplicadas e os dados iniciais foram carregados com sucesso através do script de seed.