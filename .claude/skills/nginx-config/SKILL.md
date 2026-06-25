---
name: nginx-config
description: Use this skill when writing or editing Nginx configuration for the LegisKids project — serving the built Vue/static frontend, reverse-proxying API requests to the Flask backend, HTTPS/TLS setup, or caching/headers. Triggers on nginx.conf, default.conf, or questions about reverse proxy/static file serving in production. For the Docker image that packages this config, also consult docker-containers.
---

# Nginx — Servindo o LegisKids em Produção

## Papel do Nginx na arquitetura

Nginx serve dois propósitos no LegisKids: (1) servir os arquivos estáticos do build do frontend (HTML/CSS/JS gerado pelo Vite ou as páginas vanilla), e (2) atuar como **reverse proxy**, repassando requisições de `/api/*` para o backend Flask (via Gunicorn), de forma que o navegador veja tudo como uma única origem.

## Configuração base

```nginx
# nginx.conf
server {
    listen 80;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    # Arquivos estáticos do build (JS/CSS com hash no nome) — cache agressivo,
    # pois o hash no nome do arquivo já muda quando o conteúdo muda.
    location ~* \.(?:js|css|woff2?|png|jpg|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Suporte a SPA com Vue Router em modo history: qualquer rota desconhecida
    # cai no index.html, e o Vue Router decide o que renderizar no cliente.
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Proxy reverso para o backend Flask/Gunicorn
    location /api/ {
        proxy_pass http://backend:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Pontos importantes:
- `try_files $uri $uri/ /index.html;` é essencial para SPAs com Vue Router usando `createWebHistory()` — sem isso, recarregar a página em `/proposicoes/42` retorna 404 do Nginx, porque esse path não existe como arquivo real no disco.
- `backend:5000` no `proxy_pass` assume que o Nginx está no mesmo `docker-compose` que o serviço `backend` (resolução de nome via rede interna do Docker, ver skill `docker-containers`) — em produção fora do Compose, isso seria o hostname/IP real do backend.
- Cabeçalhos `X-Forwarded-*` repassados para o Flask poder saber o IP real do cliente e o protocolo original (HTTP/HTTPS), úteis para logging e para qualquer lógica que dependa disso.
- Cache longo (`expires 1y`) só é seguro porque o processo de build do Vite gera nomes de arquivo com hash do conteúdo — nunca aplique cache tão agressivo a `index.html` (que deve sempre buscar a versão mais recente).

## HTTPS/TLS

Em produção, sempre forçar HTTPS e redirecionar HTTP -> HTTPS:

```nginx
server {
    listen 80;
    server_name legiskids.exemplo.org;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name legiskids.exemplo.org;

    ssl_certificate     /etc/letsencrypt/live/legiskids.exemplo.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/legiskids.exemplo.org/privkey.pem;

    # ... resto da configuração igual ao bloco base acima
}
```

Use Let's Encrypt/Certbot (ou o provisionamento de TLS da plataforma de hospedagem, se houver) em vez de certificados autoassinados em produção.

## Cabeçalhos de segurança

```nginx
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

- `X-Frame-Options: DENY` evita que o site seja embutido em um `<iframe>` de outro domínio (mitigação de clickjacking).
- `X-Content-Type-Options: nosniff` evita que o navegador tente "adivinhar" o tipo de conteúdo de um arquivo, reduzindo certos vetores de XSS.

## Limites e timeouts

Para evitar que um upload ou requisição mal-formada consuma recursos indefinidamente:

```nginx
client_max_body_size 5m;
proxy_read_timeout 30s;
proxy_connect_timeout 10s;
```

Ajuste `client_max_body_size` conforme o maior payload legítimo esperado (ex.: se houver upload de algum documento relacionado a uma proposição); não deixe no valor default sem pensar no caso de uso real.

## Logs

```nginx
access_log /var/log/nginx/access.log;
error_log  /var/log/nginx/error.log warn;
```

Mantenha logs de acesso e erro separados, com nível `warn` ou mais alto para o error log em produção (evita ruído excessivo de avisos triviais).

## Checklist

1. `try_files ... /index.html` configurado para suportar rotas do Vue Router em modo history.
2. `/api/` com `proxy_pass` correto para o backend, repassando cabeçalhos `X-Forwarded-*`.
3. HTTPS forçado em produção, com redirecionamento 301 de HTTP.
4. Cabeçalhos de segurança básicos presentes (`X-Frame-Options`, `X-Content-Type-Options`).
5. `client_max_body_size` e timeouts definidos deliberadamente, não deixados no default sem revisão.
