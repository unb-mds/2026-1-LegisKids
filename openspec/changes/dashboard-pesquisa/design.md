## Context

O frontend do LegisKids é HTML + CSS + JavaScript puro (sem framework, sem build). O `dashboard-principal` (`index.html`) já está implementado e define os tokens de design globais em `frontend/css/style.css`. A tela de pesquisa é uma página secundária que herda esses tokens e adiciona apenas os componentes específicos de busca.

O spec visual completo está em `specs/spec.json` e define tokens de cor, componentes e comportamento responsivo. O princípio arquitetural do projeto determina que **o frontend nunca acessa a API da Câmara dos Deputados diretamente** — todos os dados vêm do backend Flask via Fetch API. Nesta change, os dados são mock; a estrutura já deve estar pronta para substituição por `fetch('/api/proposicoes?q=...')`.

## Goals / Non-Goals

**Goals:**
- Reproduzir fielmente todos os componentes definidos em `spec.json`: navbar, search bar grande, search summary card, toolbar, result cards e paginação.
- Herdar os tokens de design de `style.css` sem duplicar variáveis CSS — `pesquisa.css` contém apenas estilos exclusivos desta página.
- Implementar leitura da query via `URLSearchParams` (`?q=Cyberbullying`) para receber o termo digitado no dashboard principal.
- Implementar filtro em tempo real, ordenação multi-critério (recentes, antigos, urgência, alfabético) e paginação cliente-side.
- Implementar empty state quando a busca refinada não retorna resultados.
- Usar SVG inline para todos os ícones (sem dependência de arquivos externos).

**Non-Goals:**
- Integração com backend real — fica para a próxima task da Release 1.
- Modal lateral de filtros — marcado como TODO no JS; escopo de change futura (US09 completo).
- Histórico de buscas por usuário — requer autenticação (Release 2, US08 complemento).
- Outros pages (projetos.html, alertas.html, analises.html).

## Decisions

### 1. CSS isolado em `pesquisa.css`, tokens herdados de `style.css`

**Decisão:** `pesquisa.css` importa apenas estilos exclusivos desta página. Todos os tokens (`--primary`, `--radius-lg`, `--shadow`, etc.) são herdados de `style.css`, que já define o `:root`.

**Rationale:** Evita duplicação de variáveis e garante que mudanças globais de tema se propagam automaticamente para a tela de pesquisa.

### 2. Query lida via `URLSearchParams` na inicialização

**Decisão:** O JS lê `?q=` da URL ao carregar a página e preenche o campo de busca com esse valor.

**Rationale:** Permite que o dashboard principal navegue para `pesquisa.html?q=Cyberbullying` e a tela já inicie com os resultados filtrados, sem JavaScript adicional no `index.html`. Quando o backend estiver disponível, basta trocar o mock por `fetch('/api/proposicoes?q=' + encodeURIComponent(query))`.

### 3. Paginação cliente-side sobre o mock

**Decisão:** A paginação é renderizada em JavaScript com um algoritmo de janela deslizante (páginas 1, 2, atual±1, penúltima, última com reticências entre gaps).

**Rationale:** O mock tem 3 itens mas o spec define `resultsCount: 23` — a paginação demonstra o comportamento real esperado sem precisar de dados reais, e o algoritmo já está pronto para ser alimentado pela paginação real do backend.

### 4. Ordenação multi-critério no cliente

**Decisão:** O dropdown de ordenação (recentes, antigos, urgência, alfabético) opera sobre os resultados já filtrados, sem nova chamada de API.

**Rationale:** Com mock data, não há backend para ordenar. A implementação no cliente é um bom proxy que serve de documentação do comportamento esperado quando a ordenação for delegada para query params da API.

### 5. Componente `result-card` alinhado com `projeto-card` do dashboard

**Decisão:** Os cards de resultado usam as mesmas convenções de badge, status e hover do `projeto-card` do dashboard principal.

**Rationale:** Consistência visual entre as duas telas e facilidade de manutenção — mudanças em um componente são facilmente espelhadas no outro.

## Risks / Trade-offs

- **Mock com 3 itens vs. spec com 23 resultados:** a paginação reflete o total do spec (23), mas a lista visível tem apenas 3 itens. Aceitável nesta fase; quando o backend retornar dados reais, o total e a lista serão substituídos juntos.
- **Filtro em tempo real no cliente pode divergir do backend:** o filtro mock usa `includes()` simples. A busca real do backend pode ter stemming, relevância ou full-text. Mitigado documentando o TODO de substituição no JS.
- **Navbar colapsada no mobile sem menu hambúrguer:** mesmo comportamento do dashboard principal — menu some no mobile por ora. Menu responsivo completo é escopo de change futura (US17).

## Migration Plan

1. Implementar `pesquisa.html`, `pesquisa.css` e `pesquisa.js` com mock data. *(done)*
2. Quando o backend Flask tiver o endpoint `/api/proposicoes?q=&page=&per_page=`, substituir `MOCK_RESULTS` em `pesquisa.js` por `fetch()` correspondente e alimentar a paginação com `total_pages` retornado pela API.
3. Quando o endpoint de filtros estiver disponível, implementar o modal de filtros (US09) mapeando os parâmetros da UI para query params da API.
4. Quando os assets de imagem estiverem disponíveis em `frontend/assets/`, substituir os SVGs inline pelos `<img>` referenciados no spec.

## Open Questions

- O modal de filtros (US09) será um drawer lateral ou um painel inline acima da lista de resultados?
- A paginação real virá com cursor-based ou offset/page?
- A busca semântica (backend) retorna scores de relevância para ordenar por "mais relevante"?
