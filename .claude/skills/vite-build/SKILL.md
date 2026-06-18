---
name: vite-build
description: Use this skill when configuring Vite for the LegisKids Vue frontend — vite.config.js, environment variables (import.meta.env), dev server proxy to the Flask backend, or build/bundling settings. Triggers on vite.config.js/ts, .env files for the frontend, or questions about the dev server/build process.
---

# Vite — Build do Frontend LegisKids

## Configuração base

```javascript
// vite.config.js
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "node:path";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:5000",
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: "dist",
    sourcemap: false,
  },
});
```

Pontos importantes:
- Alias `@` -> `src/` evita imports relativos longos (`../../../components/X.vue`) e é o padrão que outras skills do projeto (Vue, Pinia, Router) já assumem nos exemplos (`@/services/api`, `@/stores/auth`).
- `server.proxy` redireciona chamadas `/api/*` do dev server do Vite para o Flask rodando em `localhost:5000` — assim o frontend em desenvolvimento pode usar URLs relativas (`/api/proposicoes`) iguais às de produção, sem precisar de CORS configurado em dev nem hardcode de `http://localhost:5000` no código JS.
- `sourcemap: false` em build de produção, a menos que precise debugar produção diretamente — reduz tamanho e não expõe código-fonte mapeado publicamente.

## Variáveis de ambiente

Vite só expõe ao código do cliente variáveis prefixadas com `VITE_`:

```bash
# .env (não commitado)
VITE_API_BASE_URL=/api
VITE_GOOGLE_CLIENT_ID=seu-client-id.apps.googleusercontent.com
```

```javascript
const baseUrl = import.meta.env.VITE_API_BASE_URL;
```

- Nunca coloque segredos reais (chaves de API privadas, secrets) em variáveis `VITE_*` — qualquer coisa com esse prefixo é embutida no bundle final e fica visível a qualquer pessoa no navegador. `VITE_GOOGLE_CLIENT_ID` é seguro porque o client ID do Google é público por design (ver skill `google-oauth`); uma `GEMINI_API_KEY`, por exemplo, nunca deveria ter o prefixo `VITE_` nem existir no frontend.
- Mantenha um `.env.example` no repositório documentando as chaves esperadas, sem valores reais.

## Build de produção

```bash
npm run build      # gera dist/ com assets com hash de conteúdo no nome
npm run preview     # serve o build de produção localmente para verificação
```

O `dist/` gerado é o que entra na imagem Docker do frontend (ver skill `docker-containers`), servido por Nginx — Vite não roda em produção, apenas gera os arquivos estáticos finais.

## Otimizações comuns

- Code-splitting já é automático por rota se as views forem importadas com `() => import(...)` no Vue Router (ver skill `vue-router`) — não é preciso configuração extra no Vite para isso.
- Para dependências grandes usadas só em uma parte da aplicação (ex.: Chart.js, se não for usado em toda página), confirme que o import dinâmico realmente isola esse código em um chunk separado, inspecionando a saída de `npm run build` (lista de chunks gerados e seus tamanhos).

## Checklist

1. Alias `@` configurado para `src/`, usado de forma consistente nos imports.
2. Proxy de `/api` para o Flask configurado no dev server, evitando CORS/URLs hardcoded em dev.
3. Apenas variáveis realmente públicas usam o prefixo `VITE_*`.
4. `.env.example` documentando as variáveis esperadas, sem segredos reais.
5. Build de produção (`dist/`) é o artefato servido por Nginx, nunca o dev server do Vite em produção.
