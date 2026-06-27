## ADDED Requirements

### Requirement: Projeto Vue 3 inicializado com Vite
O sistema SHALL possuir um projeto Vue 3 na pasta `frontend/`, criado via `npm create vue@latest`, com Vue Router e Pinia habilitados durante o scaffolding, e Chart.js instalado manualmente.

#### Scenario: Estrutura de pastas correta
- **WHEN** o desenvolvedor clona o repositório e acessa `frontend/`
- **THEN** deve existir `package.json`, `vite.config.js`, `index.html`, `src/main.js`, `src/App.vue` e `src/assets/`

#### Scenario: Servidor de desenvolvimento funciona
- **WHEN** o desenvolvedor executa `npm install && npm run dev` dentro de `frontend/`
- **THEN** o Vite inicia em `http://localhost:5173` sem erros e exibe a aplicação Vue

#### Scenario: Build de produção bem-sucedido
- **WHEN** o desenvolvedor executa `npm run build` dentro de `frontend/`
- **THEN** é gerada a pasta `frontend/dist/` com `index.html` e assets otimizados

### Requirement: Dependências corretas no package.json
O `frontend/package.json` SHALL listar como dependências de produção: `vue@^3`, `vue-router@^4`, `pinia`, `chart.js`. Como devDependencies: `vite`, `@vitejs/plugin-vue`.

#### Scenario: Instalação limpa funciona
- **WHEN** o desenvolvedor executa `npm install` em `frontend/`
- **THEN** todas as dependências são instaladas sem conflitos de versão

### Requirement: Variáveis de ambiente para a URL da API
O projeto SHALL ler a URL base do backend Flask via variável de ambiente `VITE_API_BASE_URL`, com fallback para `http://localhost:5000`.

#### Scenario: Variável de ambiente configurada
- **WHEN** existe `frontend/.env` com `VITE_API_BASE_URL=http://localhost:5000`
- **THEN** todas as chamadas de `src/services/` usam essa URL como base

#### Scenario: Sem arquivo .env
- **WHEN** não existe `frontend/.env`
- **THEN** os services usam `http://localhost:5000` como fallback padrão

### Requirement: Identidade visual preservada via CSS global
O projeto SHALL importar em `src/assets/main.css` as variáveis CSS da identidade visual do projeto (paleta de cores, fontes Cinzel e Inter, espaçamentos base), tornando-as disponíveis globalmente para todos os componentes.

#### Scenario: Variáveis CSS disponíveis nos componentes
- **WHEN** um componente `.vue` usa `var(--primary)` ou `var(--bg)` em seu `<style scoped>`
- **THEN** a cor correta da paleta institucional é aplicada, sem necessidade de redeclarar a variável
