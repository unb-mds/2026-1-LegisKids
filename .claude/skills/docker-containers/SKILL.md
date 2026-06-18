---
name: docker-containers
description: Use this skill whenever creating or editing Dockerfiles or docker-compose.yml for the LegisKids project — containerizing the Flask backend, the frontend, and PostgreSQL for local development or deployment. Triggers on Dockerfile, docker-compose.yml, "container", "Docker", or questions about running the stack locally with containers. For Nginx-specific reverse proxy config use nginx-config; for CI pipelines that build these images use github-actions-ci.
---

# Docker — LegisKids

## Visão geral da stack containerizada

```
docker-compose.yml
├── backend   (Flask + SQLAlchemy)
├── frontend  (build estático servido por Nginx, ou Vite dev server em dev)
└── db        (PostgreSQL com volume persistente)
```

## Dockerfile do backend (Flask)

```dockerfile
# backend/Dockerfile
FROM python:3.12-slim AS base

WORKDIR /app

# Camada de dependências separada do código — cache do Docker reaproveitado
# enquanto requirements.txt não mudar, mesmo que o código mude.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=wsgi.py
EXPOSE 5000

# Em produção, nunca use o servidor de desenvolvimento do Flask.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "wsgi:app"]
```

Pontos importantes:
- `COPY requirements.txt` antes de `COPY . .` — qualquer mudança no código não invalida a camada de instalação de dependências, acelerando rebuilds.
- `python:3.12-slim` em vez da imagem completa — imagem final menor.
- `gunicorn` (não `flask run`) como servidor de produção; `flask run` é só para desenvolvimento local.
- Nunca copie `.env` para dentro da imagem — variáveis de ambiente devem ser injetadas em runtime (`docker-compose.yml`/secrets do orquestrador).

## Dockerfile do frontend

Se o frontend usa Vite/Vue com build estático:

```dockerfile
# frontend/Dockerfile
FROM node:20-slim AS build
WORKDIR /app
COPY package*.json .
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

Multi-stage build: a imagem final só tem o Nginx + os arquivos estáticos gerados, não o Node.js inteiro nem `node_modules` — bem menor e com menos superfície de ataque.

## docker-compose.yml para desenvolvimento

```yaml
services:
  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: legiskids
      POSTGRES_USER: legiskids
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U legiskids"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    restart: unless-stopped
    environment:
      DATABASE_URL: postgresql://legiskids:${DB_PASSWORD}@db:5432/legiskids
      GEMINI_API_KEY: ${GEMINI_API_KEY}
      SECRET_KEY: ${SECRET_KEY}
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "5000:5000"

  frontend:
    build: ./frontend
    restart: unless-stopped
    ports:
      - "8080:80"
    depends_on:
      - backend

volumes:
  pgdata:
```

Pontos importantes:
- `depends_on` com `condition: service_healthy` no banco — evita o backend tentar conectar antes do Postgres estar de fato pronto para aceitar conexões (apenas "container iniciado" não significa "banco pronto").
- Senhas/segredos vêm de variáveis de ambiente (`${DB_PASSWORD}`), lidas de um `.env` **não commitado**, nunca hardcoded no `docker-compose.yml`.
- Volume nomeado (`pgdata`) para persistir dados do Postgres entre `docker compose down`/`up`.

## `.dockerignore`

Sempre crie, para não inflar a imagem nem expor segredos:

```
# backend/.dockerignore
venv/
__pycache__/
*.pyc
.env
.git/
tests/
```

```
# frontend/.dockerignore
node_modules/
dist/
.env
.git/
```

## Comandos do dia a dia

```bash
docker compose up -d --build     # build + sobe tudo em background
docker compose logs -f backend   # acompanhar logs de um serviço
docker compose exec backend flask db upgrade   # rodar migração dentro do container
docker compose down -v           # derruba tudo e remove volumes (cuidado: apaga dados do banco)
```

## Checklist

1. Dependências instaladas em camada separada do código-fonte (cache eficiente).
2. Servidor de produção real no CMD do backend (`gunicorn`), não o dev server do Flask.
3. Multi-stage build no frontend, imagem final sem Node.js.
4. Segredos via variáveis de ambiente/`.env` não commitado, nunca hardcoded.
5. `healthcheck` no banco + `depends_on: condition: service_healthy` no backend.
6. `.dockerignore` presente em cada serviço.
