# Checando compatibilidade entre tecnologias escolhidas

Este documento analisa a compatibilidade entre as tecnologias escolhidas para o projeto, identificando possíveis conflitos e soluções práticas.

---

## Tecnologias definidas

### Frontend

- HTML
- CSS
- JavaScript
- Fetch API para comunicação com o backend

### Backend

- Python
- Flask

### Banco de Dados

- PostgreSQL *(em validação final)*
- SQLAlchemy
- psycopg

### IA

- spaCy / transformers *(ainda em estudo para definição final)*

---

## Compatibilidade do frontend

O frontend utiliza tecnologias nativas do navegador, o que garante compatibilidade com qualquer backend capaz de expor rotas HTTP e retornar dados em JSON.

A Fetch API permite comunicação direta com APIs REST, sendo compatível com frameworks Python modernos.

Compatível com:

- Flask
- PostgreSQL indiretamente via backend (o frontend nunca acessa o banco diretamente, apenas via backend)

---

## Compatibilidade entre frontend e backend

A comunicação entre frontend e backend será feita por:

- requisições HTTP
- API REST
- respostas em JSON

Fluxo esperado:

```
Frontend (JavaScript)
↓
Fetch API
↓
Backend Python
↓
Resposta JSON
↓
Frontend atualiza interface
```

Flask oferece suporte nativo para criação de APIs e tratamento de requisições HTTP. A serialização de objetos complexos deve ser tratada manualmente ou com bibliotecas auxiliares.

Portanto: **HTML/CSS/JS + Fetch é compatível com Flask.**

---

## Compatibilidade com banco de dados

Python possui suporte estável para PostgreSQL por meio das bibliotecas:

- `psycopg`
- `SQLAlchemy`

Ambas são compatíveis com Flask.

Portanto: **Python + PostgreSQL é totalmente compatível.**

---

## Compatibilidade com IA

As bibliotecas avaliadas são:

- spaCy
- transformers

Ambas possuem suporte para:

- Python 3.10+
- integração com Flask
- processamento de texto em português (transformers suporta português dependendo do modelo escolhido, como BERTimbau)

A IA será executada no backend:

```
Backend Python
↓
Biblioteca NLP
↓
Processamento
↓
Banco PostgreSQL
```

Portanto: **IA compatível com backend em Python.**

---

## Compatibilidade com API externa

O sistema utilizará APIs públicas do governo para coleta de dados:

- API legislativa da Câmara
- API legislativa do Senado

A integração será feita por requisições HTTP e consumo de JSON, utilizando:

- `requests`
- `httpx`

Portanto: **Python possui integração direta com APIs governamentais.**

---

## Versões recomendadas

### Linguagem

- Python 3.11+

### Backend

- Flask 3.x

### Banco de Dados

- PostgreSQL 15+

### IA

- spaCy 3.x ou transformers 4.x

### Frontend

- JavaScript ES6+

---

## Possíveis conflitos e limitações

### 1. CORS entre frontend e backend

Se o frontend e o backend rodarem em portas ou domínios diferentes, o navegador pode bloquear as requisições por política de segurança.

Exemplo:

```
Frontend → localhost:3000
Backend  → localhost:5000
```

Isso pode gerar o erro:

```
Blocked by CORS policy
```

#### Opção A — habilitar CORS no Flask

Usar Flask-CORS. Simples e rápida, boa para protótipos e MVP.

#### Opção B — servir tudo pelo mesmo domínio

Backend entrega o frontend. Elimina CORS, boa para produção simples.

#### Opção C — usar reverse proxy

Com Nginx. Profissional, escalável e seguro, boa para produção real.

#### Melhor escolha prática

Provavelmente não iremos separar o frontend e backend em domínios diferentes, mas por efeito de planejamento, o ideal seria usar Flask-CORS.

---

### 2. Consumo de memória com IA

A biblioteca transformers pode exigir muita RAM, mais processamento e maior tempo de resposta, podendo causar lentidão ou travamentos em máquinas modestas.

#### Opção A — usar spaCy

Leve, rápido e simples. Ideal para classificação básica e extração de entidades.

#### Opção B — modelos menores com transformers

Exemplos: DistilBERT e MiniLM. Melhor precisão com menor custo.

#### Opção C — usar API externa

Exemplos: OpenAI API e Hugging Face Inference API. Sem peso local e escalável, porém com custo financeiro.

#### Opção D — microserviço separado

IA em serviço próprio:

```
Flask → serviço IA → resposta
```

Desacopla o sistema e facilita manutenção.

#### Melhor escolha prática

Ainda precisamos estudar para tomar essa decisão, mas a princípio, spaCy ou APIs externas seriam boas escolhas.

---

### 3. Serialização de objetos do banco

O SQLAlchemy retorna objetos Python que não podem ser enviados diretamente como JSON:

```
TypeError: Object is not JSON serializable
```

#### Opção A — conversão manual

Converter objeto em dict. Simples, porém repetitivo.

#### Opção B — usar Marshmallow

Elegante e padronizado.

#### Opção C — usar Pydantic

Validação forte e moderno.

#### Opção D — trocar Flask por FastAPI

JSON automático, integração melhor com IA e validação nativa.

#### Melhor escolha prática

Flask + SQLAlchemy + Marshmallow.

---

### 4. Latência de APIs externas

Ao consultar APIs públicas do governo, riscos incluem:

- a API pode ficar lenta ou indisponível
- mudanças no formato JSON podem quebrar o sistema

#### Opção A — cache local

Com Redis. Acelera o sistema e reduz chamadas.

#### Opção B — salvar dados no banco

Guardar respostas no PostgreSQL. Oferece histórico e resiliência.

#### Opção C — fila assíncrona

Com Celery. Processamento em segundo plano.

#### Opção D — tarefas agendadas

Atualizar dados periodicamente, por exemplo todo dia às 02:00.

#### Melhor escolha prática

Salvar dados no banco com tarefas agendadas (opções B + D).

---

### 5. Escalabilidade do Flask

O Flask é ótimo para projetos pequenos, mas em cargas maiores pode exigir cache, filas, workers e balanceamento.

#### Opção A — manter Flask

Com Gunicorn e Nginx. Suficiente para médio porte.

#### Opção B — trocar para FastAPI

Mais rápido, melhor async e ótimo para IA.

#### Opção C — arquitetura de microserviços

Separar frontend, backend, IA e coleta em serviços distintos. Boa para crescimento grande.

#### Melhor escolha prática

Não projetamos que o projeto cresça ao ponto do Flask ficar obsoleto, mas no caso hipotético, seria usar Flask com Gunicorn e Nginx.

---

### 6. Compatibilidade de versões

Bibliotecas podem ter conflitos entre versões, gerando erros como:

```
ImportError
DeprecationWarning
```

#### Opção A — requirements.txt

```
Flask==3.0.2
SQLAlchemy==2.0.25
```

#### Opção B — virtualenv

Ambiente isolado por projeto.

#### Opção C — Docker

Ambiente reproduzível que evita conflitos.

#### Melhor escolha prática

Docker + requirements.txt.

---

### 7. Segurança da API

Se a API for pública sem proteção, os riscos incluem acesso indevido, abuso de requisições e vazamento de dados.

#### Opção A — autenticação JWT

JSON Web Token.

#### Opção B — rate limiting

Com Flask-Limiter.

#### Opção C — validação de entrada

Com Marshmallow ou Pydantic.

#### Opção D — HTTPS

Via Nginx.

#### Melhor escolha prática

JWT + validação + rate limiting.

---

## Conclusão

A análise demonstra que o conjunto de tecnologias proposto apresenta **compatibilidade técnica adequada para o desenvolvimento do sistema**, com boa integração entre as camadas de frontend, backend, banco de dados, inteligência artificial e consumo de APIs externas.

No frontend, o uso de HTML, CSS, JavaScript e Fetch API oferece uma base simples e estável, permitindo comunicação eficiente com o backend via requisições HTTP e respostas em JSON. No backend, Python com Flask mostra-se compatível com a construção de APIs REST, com integração consolidada com PostgreSQL por meio de psycopg e SQLAlchemy.

Para o processamento inteligente, tanto spaCy quanto transformers são opções viáveis dentro do ecossistema Python. A escolha final deverá considerar o equilíbrio entre desempenho, consumo de recursos e complexidade das análises desejadas.

Também foram identificadas limitações técnicas previsíveis, como:

- necessidade de configuração de CORS se frontend e backend estiverem em domínios diferentes
- consumo elevado de recursos em modelos de IA mais robustos
- serialização de objetos do banco para JSON
- dependência de APIs externas
- controle de versões
- segurança da API

Todos esses pontos possuem soluções práticas já conhecidas:

- Flask-CORS para comunicação entre domínios
- Marshmallow para serialização
- Docker para padronização do ambiente
- JWT para autenticação
- Nginx para proxy e segurança
- armazenamento local e agendamento para reduzir dependência de APIs externas

As principais decisões que ainda precisam ser aprofundadas antes da implementação são:

- definição final do PostgreSQL como banco de dados
- escolha entre spaCy ou transformers
- validação do nível de processamento de IA necessário para o sistema

---

## Lista de tecnologias

| Tecnologia | Onde se encontra | Propósito | Prioridade |
| --- | --- | --- | --- |
| HTML | Frontend | Estrutura das páginas e interface | Alta |
| CSS | Frontend | Estilização visual da interface | Alta |
| JavaScript | Frontend | Interatividade da interface | Alta |
| Fetch API | Frontend | Comunicação com o backend via HTTP | Alta |
| Python | Backend | Linguagem principal da lógica do sistema | Alta |
| Flask | Backend | Criação da API REST | Alta |
| PostgreSQL *(provavelmente)* | Banco de Dados | Armazenamento estruturado dos dados | Alta |
| SQLAlchemy | Backend | ORM para integração com banco | Alta |
| psycopg *(provavelmente)* | Backend | Driver de conexão com PostgreSQL | Alta |
| spaCy *ou* transformers | Backend / IA | Processamento de linguagem natural | Média |
| requests / httpx | Backend | Consumo de APIs externas | Média |
| Marshmallow | Backend | Serialização de objetos para JSON | Média |
| Docker | Infraestrutura | Padronização do ambiente | Média |
| Flask-CORS | Backend | Permitir comunicação entre frontend e backend em domínios diferentes | Baixa |
| JWT | Segurança | Autenticação da API | Baixa |
| Flask-Limiter | Segurança | Controle de abuso de requisições | Baixa |
| Nginx | Infraestrutura | Proxy reverso e segurança | Baixa |

As tecnologias de prioridade Alta são o mínimo necessário para o sistema funcionar. Com as de prioridade Média, o projeto fica bastante robusto. As de prioridade Baixa começam a fugir do escopo atual, mas estão listadas para o caso de o projeto avançar além do previsto.