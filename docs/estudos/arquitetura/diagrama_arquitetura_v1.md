# Diagrama da Arquitetura do Projeto v1
LINK DO FIGMA: https://www.figma.com/board/grHtXIYgH7mLa7bEH8CoOa/arquitetura_diagrama_v1?node-id=0-1&t=NP3GMVch7bqPS6FH-1**
Esse diagrama será feito com base na estrutura base do Projeto, para facilitar o entediimento e desenvolvimento. Com o decorrer das Sprints, vamos atualizando o diagrama de acordo com as necessidades que vermos.

Com as Tecnologias de base definidas:

Frontend: HTML + CSS + JavaScript + Fetch

Backend: Python + Flask

IA: spaCy / transformers (ainda falta estudo e decisão)

Banco: PostgreSQL (ainda decidindo) + SQLAlchemy + psycopg 

Vamos buscar uma arquitetura:

- simples
- profissional
- escalável o suficiente
- compatível com o escopo
- de fácil compreensão

A arquitetura escolhida será baseada em camadas, com separação de responsabilidades entre interface, lógica de negócio, processamento inteligente e persistência de dados.

Camadas, simplificado:

1. Interface (Front-End) - Dashboards, Filtros e Visualização
2. Camada de Aplicação - Controller (Recebe requisições e controla o fluxo)
3. Camada de Negócios - Service (Regras de negócio, NLP e Classificação)
4. Camada de Dados - Repository (Banco de Dados e API externa)
5. Infraestrutura - Banco e Configurações

# Fluxo

## Fluxo do Sistema

O funcionamento geral do sistema será:

```jsx
Usuário
↓
Frontend (HTML/CSS/JavaScript)
↓
Fetch API
↓
Backend (Flask)
↓
Services
↓
Repositories
↓
Banco de Dados
↓
Resposta ao usuário
```

## Fluxo do Usuário

O fluxo de interação do usuário será:

```
Usuário
↓
Acessa dashboard
↓
Frontend envia requisição
↓
Backend processa
↓
Banco retorna dados
↓
Frontend atualiza interface
↓
Usuário visualiza informações
```

### Etapas

- O usuário acessa a interface web
- O frontend realiza uma requisição usando **Fetch API**
- O backend recebe a requisição
- O sistema consulta o banco
- Os dados são enviados em **JSON**
- O frontend atualiza a interface dinamicamente

## Fluxo de Dados

O fluxo interno de atualização dos dados será:

```
Scheduler
↓
Backend
↓
API governamental
↓
IA processa
↓
Banco atualizado
```

A IA terá uma agenda que todo dia, em um certo horário, irá consultar a API e atualizar o banco de dados. Dessa forma, a experiência do usuário fica mais rápida, e o software mais flúido.

# Estrutura

A estrutura inicial do projeto será organizada da seguinte forma:

```
project/
├── frontend/
├── backend/
│   ├── controllers/
│   ├── services/
│   ├── repositories/
│   ├── ai/
│   ├── models/
│   └── config/
└── database/
```

## Organização das pastas

### frontend/

Responsável por:

- interface do usuário
- páginas
- estilos
- scripts
- comunicação com backend

### backend/controllers/

Responsável por:

- receber requisições HTTP
- validar entradas
- direcionar o fluxo do sistema

### backend/services/

Responsável por:

- regras de negócio
- processamento principal
- integração entre módulos

### backend/repositories/

Responsável por:

- acesso ao banco
- acesso à API externa

### backend/ai/

Responsável por:

- classificação de proposições
- NLP
- automação inteligente

### backend/models/

Responsável por:

- representação das entidades do sistema

### backend/config/

Responsável por:

- configurações gerais
- credenciais
- parâmetros da aplicação

### database/

Responsável por:

- scripts SQL
- migrações
- estrutura do banco

# Justificativa da Arquitetura

A arquitetura foi escolhida porque:

- mantém o sistema simples para o escopo atual
- facilita manutenção futura
- separa responsabilidades
- permite crescimento moderado
- torna o projeto mais compreensível para a equipe

Essa abordagem oferece um equilíbrio entre simplicidade e organização profissional

Este diagrama será construído com base na estrutura inicial do projeto, com o objetivo de facilitar o entendimento da organização interna do sistema e apoiar o desenvolvimento.

Ao longo das Sprints, o diagrama poderá ser atualizado conforme novas necessidades forem identificadas.

---

## Tecnologias definidas

### Frontend

- HTML
- CSS
- JavaScript
- Fetch API

### Backend

- Python
- Flask

### IA

- spaCy / transformers *(ainda em estudo para definição final)*

### Banco de Dados

- PostgreSQL *(em validação final)*
- SQLAlchemy
- psycopg

---

## Objetivos da arquitetura

A arquitetura será planejada para ser:

- simples
- profissional
- escalável o suficiente
- compatível com o escopo
- de fácil compreensão

---

# Arquitetura escolhida

A arquitetura será baseada em **camadas**, com separação de responsabilidades entre:

- interface
- controle
- negócio
- processamento inteligente
- persistência de dados

---

## Camadas do sistema

### 1. Interface

Responsável por:

- dashboards
- filtros
- visualização

---

### 2. Aplicação

Responsável por:

- rotas
- controllers
- controle do fluxo

---

### 3. Negócio

Responsável por:

- regras de negócio
- validações
- processamento interno

---

### 4. Dados

Responsável por:

- acesso ao banco
- acesso à API externa

---

### 5. Infraestrutura

Responsável por:

- banco
- configurações
- autenticação externa

---

# Fluxos

## Fluxo principal do sistema

O funcionamento principal do sistema será:

```
Usuário
↓
Frontend (HTML/CSS/JavaScript)
↓
Fetch API
↓
Backend (Flask)
↓
Routes
↓
Controller
↓
Service
↓
Repository
↓
Banco de Dados
↓
Resposta JSON
↓
Frontend
```

---

## Fluxo de interação do usuário

O fluxo de consulta do usuário será:

```
Usuário
↓
Acessa dashboard
↓
Frontend envia requisição
↓
Backend recebe
↓
Controller processa
↓
Service aplica regra
↓
Repository consulta banco
↓
Banco retorna dados
↓
Frontend atualiza interface
↓
Usuário visualiza informações
```

---

### Etapas

- O usuário acessa a interface web
- O frontend realiza uma requisição usando **Fetch API**
- O backend recebe a requisição
- A rota identifica o endpoint solicitado
- O controller direciona a execução
- O service aplica a regra necessária
- O repository consulta os dados
- O backend retorna JSON
- O frontend atualiza a interface dinamicamente

---

## Fluxo automático de dados

A atualização automática dos dados será feita por agendamento:

```
Scheduler
↓
Backend
↓
Consulta API governamental
↓
Recebe dados brutos
↓
IA processa os dados
↓
Banco de Dados atualizado
```

---

### Funcionamento

- Um agendador executará a rotina diariamente
- O backend consultará a API governamental
- Os dados serão recebidos
- A IA fará a classificação
- O banco será atualizado
- O frontend consumirá os dados já processados

Dessa forma:

- a experiência do usuário fica mais rápida
- o sistema fica mais fluido
- a IA não depende da navegação do usuário

---

## Fluxo futuro de autenticação (Gov.br)

Caso o sistema utilize autenticação via Gov.br, o fluxo será:

```
Usuário
↓
Frontend
↓
Clica em "Entrar com Gov.br"
↓
Backend / Auth
↓
Gov.br
↓
Retorno do token
↓
Backend valida token
↓
Verifica usuário no banco
↓
Cria sessão
↓
Frontend recebe autenticação
↓
Usuário logado
```

---

# Estrutura do projeto

A estrutura inicial do projeto será organizada da seguinte forma:

```
project/
├── docs/
├── frontend/
│   ├── pages/
│   ├── components/
│   ├── styles/
│   ├── scripts/
│   └── assets/
├── backend/
│   ├── auth/
│   ├── routes/
│   ├── controllers/
│   ├── services/
│   ├── repositories/
│   ├── ai/
│   ├── models/
│   └── config/
└── database/
```

---

# Organização das pastas

## frontend/

Responsável por:

- interface do usuário
- páginas
- componentes
- estilos
- scripts
- comunicação com backend

---

## backend/auth/

Responsável por:

- autenticação
- login
- integração com Gov.br
- gerenciamento de sessão

---

## backend/routes/

Responsável por:

- definir endpoints da API
- direcionar requisições
- mapear URLs para controllers

---

## backend/controllers/

Responsável por:

- receber requisições HTTP
- validar entradas
- direcionar o fluxo interno

---

## backend/services/

Responsável por:

- regras de negócio
- processamento principal
- integração entre módulos

---

## backend/repositories/

Responsável por:

- acesso ao banco
- acesso à API externa

---

## backend/ai/

Responsável por:

- classificação de proposições
- NLP
- automação inteligente

---

## backend/models/

Responsável por:

- representação das entidades do sistema

---

## backend/config/

Responsável por:

- configurações gerais
- credenciais
- parâmetros da aplicação

---

## database/

Responsável por:

- scripts SQL
- migrações
- estrutura do banco

---

# Justificativa da arquitetura

A arquitetura foi escolhida porque:

- mantém o sistema simples para o escopo atual
- facilita manutenção futura
- separa responsabilidades
- permite crescimento moderado
- melhora a organização do código
- torna o projeto mais compreensível para a equipe

Essa abordagem oferece um equilíbrio entre simplicidade e organização profissional.