## Context

O frontend do LegisKids é HTML + CSS + JavaScript puro (sem framework, sem build). A única página existente antes dessa change era um scaffold com navbar básica. O spec visual completo está em `specs/dashboard/spec.json` e define tokens de cor, layout, componentes e comportamento responsivo. O protótipo no Figma é a referência visual de alto nível.

O princípio arquitetural do projeto determina que **o frontend nunca acessa a API da Câmara dos Deputados diretamente** — todos os dados vêm do backend Flask via Fetch API. Nesta change, os dados são mock; a estrutura já deve estar pronta para substituição por `fetch('/api/...')`.

## Goals / Non-Goals

**Goals:**
- Reproduzir fielmente todos os componentes definidos em `spec.json`.
- Implementar os tokens de design como variáveis CSS (`:root`) para facilitar manutenção.
- Entregar responsividade nos três breakpoints do spec: mobile (2 colunas), tablet (2 colunas), desktop (4 colunas).
- Implementar interatividade básica com JavaScript puro: busca em tempo real, clique nas categorias da biblioteca, empty state na busca sem resultados.
- Usar SVG inline para todos os ícones (sem dependência de arquivos de imagem externos que ainda não existem).

**Non-Goals:**
- Integração com backend real — fica para a próxima task da Release 1.
- Autenticação ou sessão de usuário.
- Outros pages (projetos.html, alertas.html, analises.html) — são escopo de changes futuras.
- Gráficos ou dashboards analíticos — escopo da Release 2 (US11, US14).

## Decisions

### 1. CSS custom properties como sistema de tokens

**Decisão:** Todos os valores de cor, sombra, border-radius e transição do spec.json são mapeados para variáveis CSS em `:root`.

**Rationale:** Permite que futuras mudanças de tema sejam feitas em um único lugar e evita magic strings repetidas. Mantém consistência entre componentes.

**Alternativas consideradas:**
- CSS-in-JS ou Tailwind: descartados — o projeto não usa build pipeline e não adota framework de CSS.

### 2. Ícones SVG inline

**Decisão:** Todos os ícones são SVG inline no HTML, não dependências de arquivo externo.

**Rationale:** Os arquivos de imagem referenciados no spec (`assets/icons/*.png`) ainda não existem no repositório. SVG inline garante que a página funcione imediatamente sem assets externos, com controle total de cor via `stroke` CSS.

**Alternativas consideradas:**
- Emojis: descartados por inconsistência visual entre sistemas operacionais.
- Font icons (Font Awesome): descartada dependência de CDN adicional.

### 3. Mock data em `script.js`, não embutido no HTML

**Decisão:** Os dados mock ficam em `MOCK_PROJETOS` no JavaScript, e o HTML renderiza via atributos `data-*`.

**Rationale:** Quando o backend estiver pronto, a substituição por `fetch()` fica isolada no JS, sem tocar no HTML. O HTML é a camada de apresentação; o JS é a camada de dados.

### 4. Biblioteca Legislativa como atalho de busca

**Decisão:** Clicar em um card da Biblioteca Legislativa preenche o campo de busca com o nome da categoria e dispara o filtro.

**Rationale:** O spec define 8 cards vazios `{}` sem comportamento especificado. Esse comportamento conecta dois componentes da tela de forma intuitiva e antecipa a futura integração com filtros reais do backend (US08, US09).

## Risks / Trade-offs

- **Assets de imagem ausentes (logo, ícones):** resolvido com SVG inline nesta fase. Quando as imagens estiverem disponíveis, basta trocar os SVGs sem mudar a estrutura.
- **Dados mock divergindo do schema real da API:** mitigado documentando o formato esperado em `MOCK_PROJETOS` nos comentários do JS.
- **Navbar colapsada no mobile sem menu hambúrguer:** o menu some no mobile por ora (`display: none`). Menu responsivo completo é escopo de change futura de usabilidade (US17).

## Migration Plan

1. Implementar `index.html`, `style.css` e `script.js` com mock data. *(done)*
2. Quando o backend Flask tiver os endpoints `/api/stats` e `/api/proposicoes`, substituir `MOCK_PROJETOS` e `MOCK_STATS` em `script.js` por `fetch()` correspondentes.
3. Quando os assets de imagem estiverem disponíveis em `frontend/assets/`, substituir os SVGs inline pelos `<img>` referenciados no spec.

## Open Questions

- Os 8 cards da Biblioteca Legislativa terão dados dinâmicos (contagem por tema) ou serão categorias fixas de navegação?
- O menu mobile terá drawer/hambúrguer ou um bottom nav bar?
