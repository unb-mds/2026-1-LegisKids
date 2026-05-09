# Diagrama da Arquitetura do Projeto v2
LINK DO FIGMA: https://www.figma.com/board/5qqctfNDqw7eqWz6PsKYfS/arquitetura_diagrama_v2?node-id=0-1&t=tOb76BxZKqqiHhOT-1

Esse diagrama será feito com base na estrutura base do Projeto, para facilitar o entediimento e desenvolvimento. Com o decorrer das Sprints, vamos atualizando o diagrama de acordo com as necessidades que vermos.

Com as Tecnologias de base definidas:

- Frontend: HTML + CSS + JavaScript + Fetch
- Backend: Python + Flask
- Autentificação: OAuth 2.0 (Google)

IA: spaCy / transformers (ainda falta estudo e decisão)

Banco: PostgreSQL (ainda decidindo) + SQLAlchemy + psycopg 

Com o Fluxo de Dados e sistema de Login decididos, conseguimos montar melhor o fluxo geral do sistema, e os fluxos individuais, posteriormente.

O sistema tem como objetivo principal consumir dados públicos da Câmara dos Deputados do Brasil, tratá-los e disponibilizá-los de forma eficiente ao usuário, permitindo também personalização (favoritos, histórico e notificações).

O objetivo é estabelecer um fluxo **simples, performático e escalável o suficiente**, garantindo boa experiência para o usuário e facilidade de manutenção.

# Arquitetura do Sistema

A arquitetura será baseada em camadas, com separação clara de responsabilidades:

### Camadas

1. **Frontend (Interface)**
    - Dashboards
    - Filtros
    - Visualização
2. **Backend (Aplicação)**
    - Rotas
    - Controllers
    - Controle do fluxo
3. **Camada de Negócio (Services)**
    - Regras de negócio
    - Processamento dos dados
    - Integração com IA
4. **Camada de Dados (Repositories)**
    - Acesso ao banco de dados
    - Consumo da API externa
5. **Infraestrutura**
    - Banco de dados
    - Configurações
    - Autenticação

# Fluxo Principal do Sistema

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

O frontend **nunca acessa a API externa diretamente**.

# Fluxo do Usuário

## Login

O login será feito via Google utilizando OAuth 2.0:

```
Usuário
↓
Frontend
↓
Login com Google
↓
Backend recebe token
↓↓

Valida token
↓
Busca ou cria usuário
↓
Cria sessão
↓
Usuário autenticado
```

## Navegação

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

## Favoritos

```
Usuário favorita proposição
↓
Backend registra em favoritos (user_id, proposicao_id)
```

---

## Histórico

```
Usuário interage
↓
Backend registra evento no historico
```

## Notificações

```
Proposição é atualizada
↓
Sistema identifica usuários que favoritaram
↓
Cria notificações
↓
Usuário visualiza no sistema
```

# Fluxo de Dados (ETL)

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

Estratégia:

> Buscar o que mudou recentemente (tramitações)
> 

## Observação importante

A API não fornece atualização global.

Portanto:

- usamos tramitação como proxy de mudança
- aceitamos pequenas inconsistências pontuais

Isso é suficiente para dashboards e análise.

# Integração dos Fluxos

O sistema possui dois fluxos principais:

### 🔹 Assíncrono (dados)

- API → processamento → banco

### 🔹 Síncrono (usuário)

- login → navegação → interação

Ambos convergem no banco de dados estruturado.

# Estrutura do Sistema

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

# Estrutura de Dados

- `proposicoes` → dados tratados das proposições
- `users` → usuários
- `favoritos` → relação usuário ↔ proposição
- `historico` → interações
- `notificacoes` → eventos

Todas as relações feitas via `user_id` e `proposicao_id`.

# Síntese

O sistema não consome dados em tempo real para o usuário

Ele **prepara os dados antes** e entrega pronto

Resultado:

- alta performance
- boa experiência
- arquitetura simples e sólida