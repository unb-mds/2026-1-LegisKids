# Diagrama da Arquitetura - LegisKids v2

Link do Figma: https://www.figma.com/board/5qqctfNDqw7eqWz6PsKYfS/arquitetura_diagrama_v2?node-id=0-1&t=tOb76BxZKqqiHhOT-1

Este diagrama será construído com base na estrutura do projeto, para facilitar o entendimento e desenvolvimento. Com o decorrer das Sprints, vamos atualizando o diagrama de acordo com as necessidades identificadas.

O sistema tem como objetivo principal consumir dados públicos da Câmara dos Deputados do Brasil, tratá-los e disponibilizá-los de forma eficiente ao usuário, permitindo também personalização via favoritos, histórico e notificações.

O objetivo é estabelecer um fluxo simples, performático e escalável o suficiente, garantindo boa experiência para o usuário e facilidade de manutenção.

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

### Autenticação

- OAuth 2.0 (Google)

### IA

- spaCy / transformers *(ainda em estudo para definição final)*

### Banco de Dados

- PostgreSQL *(em validação final)*
- SQLAlchemy
- psycopg

---

## Arquitetura do sistema

A arquitetura será baseada em camadas, com separação clara de responsabilidades.

### 1. Frontend (Interface)

Responsável por:

- dashboards
- filtros
- visualização

---

### 2. Backend (Aplicação)

Responsável por:

- rotas
- controllers
- controle do fluxo

---

### 3. Negócio (Services)

Responsável por:

- regras de negócio
- processamento dos dados
- integração com IA

---

### 4. Dados (Repositories)

Responsável por:

- acesso ao banco de dados
- consumo da API externa

---

### 5. Infraestrutura

Responsável por:

- banco de dados
- configurações
- autenticação

---

## Fluxo principal do sistema

O fluxo padrão de requisição será:

```
Usuário
↓
Frontend (HTML/CSS/JS)
↓
Fetch API
↓
Backend (Flask)
↓
Routes
↓
Controllers
↓
Services
↓
Repositories
↓
Banco de Dados
↓
Resposta JSON
↓
Frontend
```

O frontend nunca acessa a API externa diretamente.

---

## Fluxos do usuário

### Login

O login será feito via Google utilizando OAuth 2.0:

```
Usuário
↓
Frontend
↓
Login com Google
↓
Backend recebe token
↓
Valida token
↓
Busca ou cria usuário
↓
Cria sessão
↓
Usuário autenticado
```

---

### Navegação

```
Usuário acessa dashboard
↓
Frontend envia requisição
↓
Backend processa
↓
Banco retorna dados já tratados
↓
Frontend renderiza
```

---

### Favoritos

```
Usuário favorita proposição
↓
Backend registra em favoritos (user_id, proposicao_id)
```

---

### Histórico

```
Usuário interage
↓
Backend registra evento no historico
```

---

### Notificações

```
Proposição é atualizada
↓
Sistema identifica usuários que favoritaram
↓
Cria notificações
↓
Usuário visualiza no sistema
```

---

## Fluxo de dados (ETL)

A atualização dos dados é feita de forma assíncrona:

```
Scheduler
↓
Backend
↓
Consulta API da Câmara dos Deputados
↓
Busca proposições com movimentação recente
↓
Para cada proposição:
    ↓
    Busca dados completos
    ↓
    Processa e normaliza
    ↓
    Classifica com IA
    ↓
    Atualiza banco
```

A estratégia adotada é buscar o que mudou recentemente via tramitações.

### Observação importante

A API não fornece atualização global. Portanto:

- usamos tramitação como proxy de mudança
- aceitamos pequenas inconsistências pontuais

Isso é suficiente para dashboards e análise.

---

## Integração dos fluxos

O sistema possui dois fluxos principais:

**Assíncrono (dados):** API → processamento → banco

**Síncrono (usuário):** login → navegação → interação

Ambos convergem no banco de dados estruturado.

---

## Estrutura do projeto

```
project/
├── frontend/
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

## Estrutura de dados

- `proposicoes` — dados tratados das proposições
- `users` — usuários
- `favoritos` — relação usuário e proposição
- `historico` — interações
- `notificacoes` — eventos

Todas as relações são feitas via `user_id` e `proposicao_id`.

---

## Síntese

O sistema não consome dados em tempo real para o usuário. Os dados são preparados previamente e entregues prontos, resultando em:

- alta performance
- boa experiência
- arquitetura simples e sólida