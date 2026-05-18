# Estudo: Banco de Dados

---

## O que é um banco de dados

Um banco de dados é uma coleção organizada de informações armazenadas eletronicamente, gerenciada por um SGBD (Sistema de Gerenciamento de Banco de Dados). Os dados nos tipos mais comuns são modelados em linhas e colunas em tabelas, tornando o processamento e a consulta eficientes.

Um banco de dados é importante porque permite:

- armazenar informações de forma segura
- recuperar e atualizar dados rapidamente
- evitar duplicidade e inconsistências
- organizar grandes volumes de informação
- realizar consultas complexas
- sustentar o crescimento do sistema

---

## Bancos relacionais (SQL)

SQL (Structured Query Language) é a linguagem usada por bancos relacionais para consultar, manipular e definir dados. Os dados são organizados em tabelas que se relacionam entre si por meio de chaves.

### Por que o SQL é importante

- é declarativo e acessível mesmo para iniciantes
- integra-se com linguagens como Python e Java
- adere às propriedades ACID (atomicidade, consistência, isolamento e durabilidade), garantindo confiabilidade em transações críticas
- amplamente usado em ciência de dados, IA e aplicações corporativas

### Componentes principais

**Tabela** — elemento básico do banco relacional, composta por linhas e colunas. Cada tabela representa um assunto específico.

**Instruções SQL** — comandos como `INSERT`, `SELECT`, `UPDATE` e `DELETE` para manipular os dados.

**Procedimentos armazenados** — coleções de instruções SQL reutilizáveis, usadas para melhorar eficiência e performance.

### Vantagens

- fácil manipulação de dados com comandos simples
- processamento rápido com índices e otimização de consultas
- segurança robusta com autenticação, controles de acesso e criptografia
- compatibilidade com padrões ANSI e ISO
- escalabilidade para bancos pequenos e grandes
- forte suporte de comunidade (muitos bancos SQL são open source)

---

## Bancos não relacionais (NoSQL)

NoSQL se refere a bancos que não usam tabelas para armazenar dados. São populares para aplicações modernas por serem horizontalmente escaláveis.

### Tipos de bancos NoSQL

**Chave-valor** — modelo mais simples, organizado como um dicionário de pares chave-valor. Usado em cache e sessões de usuário. Exemplos: Redis, Memcached.

**Armazenamento de documentos** — armazena dados como documentos JSON, XML ou BSON. Flexível para dados semi-estruturados. Exemplo: MongoDB.

**Colunas amplas** — armazena informações em colunas, permitindo acesso apenas às colunas necessárias. Usado em big data. Exemplos: Apache HBase, Apache Cassandra.

**Grafos** — armazena nós, arestas e propriedades para representar redes de conexões. Exemplo: Neo4J.

**Memória** — dados residem na memória principal em vez do disco, resultando em acesso mais rápido. Exemplo: IBM solidDB.

### Vantagens

- custo-benefício: escalabilidade horizontal sem licenças caras
- flexibilidade: modelo de dados adaptável a mudanças rápidas
- replicação: dados copiados em múltiplos servidores para maior confiabilidade
- velocidade: armazenamento e processamento mais ágeis

---

## SQL x NoSQL

|  | Bancos relacionais (SQL) | Bancos NoSQL |
| --- | --- | --- |
| Modelo de dados | Tabelas com linhas e colunas, esquema fixo | Chave-valor, documento, grafo, coluna |
| Propriedades ACID | Suporte completo | Parcial ou flexível |
| Escalabilidade | Vertical (mais hardware) | Horizontal (mais servidores) |
| Performance | Depende de índices e otimização | Depende do cluster e da latência |
| Ideal para | Transações consistentes, sistemas tradicionais | Alta escala, baixa latência, dados variáveis |

---

## Conceitos básicos

### Tabelas

Uma tabela é como uma planilha: armazena dados sobre um assunto específico em linhas e colunas.

Exemplo — tabela `Aluno`:

| id_aluno | nome | curso |
| --- | --- | --- |
| 1 | Ana | Engenharia |
| 2 | João | Computação |

### Registros

Um registro é uma linha da tabela, representando uma entrada individual. Cada linha da tabela `Aluno` representa um aluno específico.

### Chave primária (Primary Key)

Identifica cada registro de forma única. Na tabela `Aluno`, o campo `id_aluno` é a chave primária porque nunca se repete e nunca é nulo.

### Chave estrangeira (Foreign Key)

Conecta uma tabela a outra. Na tabela `Matricula`, o campo `id_aluno` é uma chave estrangeira que aponta para `Aluno.id_aluno`, criando o relacionamento entre as duas tabelas.

---

## CRUD — Operações básicas

Usando a tabela `Aluno` como exemplo:

| id_aluno | nome | curso |
| --- | --- | --- |
| 1 | Ana | Computação |
| 2 | João | Engenharia |

### CREATE — inserir dados

```sql
INSERT INTO Aluno (id_aluno, nome, curso)
VALUES (3, 'Maria', 'Medicina');
```

### READ — consultar dados

```sql
SELECT * FROM Aluno;

SELECT * FROM Aluno
WHERE id_aluno = 2;
```

### UPDATE — alterar dados

```sql
UPDATE Aluno
SET curso = 'Sistemas'
WHERE id_aluno = 1;
```

### DELETE — remover dados

```sql
DELETE FROM Aluno
WHERE id_aluno = 2;
```

---

## Normalização de dados

Normalização é o processo de organizar as tabelas para evitar repetição desnecessária e reduzir erros, guardando cada informação no lugar certo, apenas uma vez.

### Problema sem normalização

| id_pedido | cliente | telefone | produto |
| --- | --- | --- | --- |
| 1 | Ana | 9999 | Mouse |
| 2 | Ana | 9999 | Teclado |

Nome e telefone se repetem. Se Ana trocar o telefone, é necessário alterar em várias linhas — risco de inconsistência.

### Com normalização

Tabela `Cliente`:

| id_cliente | nome | telefone |
| --- | --- | --- |
| 1 | Ana | 9999 |

Tabela `Pedido`:

| id_pedido | id_cliente | produto |
| --- | --- | --- |
| 1 | 1 | Mouse |
| 2 | 1 | Teclado |

Os dados do cliente aparecem uma única vez; os pedidos apenas referenciam o cliente.

### Objetivos da normalização

- eliminar redundância
- evitar inconsistências
- melhorar manutenção e atualização
- tornar o banco mais lógico e eficiente

---

## Vídeos recomendados

Vídeos mais rápidos e gerais:

- https://www.youtube.com/watch?v=9a3xgD4SMwQ
- https://www.youtube.com/watch?v=VbNDTOGjt4o

Vídeo mais aprofundado:

- https://www.youtube.com/watch?v=XfO3TRvESBo

---

## Resumo

Um banco de dados é uma coleção organizada de informações gerenciada por um SGBD, permitindo armazenar, consultar, atualizar e controlar dados com segurança e organização.

**SQL (relacional)** — tabelas com esquema fixo, alta consistência, ideal para transações. Exemplos: PostgreSQL, MySQL.

**NoSQL (não relacional)** — formatos flexíveis (documentos, chave-valor, grafos), alta escalabilidade, ideal para aplicações modernas. Exemplos: MongoDB, Redis.

**Conceitos fundamentais:** tabela (conjunto de dados), registro (uma linha), chave primária (identificador único), chave estrangeira (relacionamento entre tabelas).

**CRUD:** Create (`INSERT`), Read (`SELECT`), Update (`UPDATE`), Delete (`DELETE`).

**Normalização:** organizar tabelas para eliminar redundância, evitar inconsistências e facilitar manutenção.