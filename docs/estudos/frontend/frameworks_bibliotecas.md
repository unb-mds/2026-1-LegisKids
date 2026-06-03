# Estudo Técnico: Frameworks e Bibliotecas para o Frontend

## Contexto

O LegisKids possui atualmente um frontend construído com **HTML5, CSS3 e JavaScript puro**, comunicando-se com o backend Flask via **Fetch API**. A abordagem vanilla foi escolhida para simplificar o início do projeto e garantir entendimento da comunicação cliente-servidor antes de adotar abstrações.

Este estudo avalia a viabilidade de adotar frameworks ou bibliotecas especializadas nas próximas releases, considerando as demandas crescentes da aplicação:

---

## Critérios de Avaliação

| Critério | Descrição |
|---|---|
| Compatibilidade com Flask | Integração com API REST e respostas JSON |
| Integração com Fetch API | Suporte ao modelo de comunicação atual |
| Organização de componentes | Reusabilidade e manutenção da interface |
| Desempenho | Tempo de carregamento, bundle size, renderização |
| Escalabilidade | Capacidade de crescer com o projeto |
| Manutenção | Facilidade de atualização e refatoração |
| Curva de aprendizado | Tempo estimado para a equipe ser produtiva |
| Suporte da comunidade | Maturidade, documentação e ecossistema |

---

## 1. Frameworks SPA (Single Page Application)

### React

React é uma biblioteca JavaScript mantida pela Meta para construção de interfaces baseadas em componentes. É o framework mais adotado do mercado.

**Pontos fortes:**

- Ecossistema massivo (bibliotecas para gráficos, roteamento, formulários, estado)
- Componentização madura com reutilização real de UI
- Virtual DOM garante atualizações eficientes na interface
- Integração natural com qualquer API REST via Fetch ou bibliotecas como `react-query`
- Excelente suporte a TypeScript

**Pontos fracos:**

- Curva de aprendizado moderada/alta: hooks, contexto, ciclo de vida de componentes, JSX
- Exige bundler (Vite, Webpack), o que adiciona complexidade ao setup
- Migração do frontend atual exigiria reescrita completa das telas existentes
- Bundle inicial mais pesado para uma aplicação pequena
- Não é compatível com servir arquivos estáticos diretamente pelo Flask sem um build step

**Compatibilidade com a arquitetura atual:**

Flask continua como backend puro. O React seria servido como SPA separada (próprio servidor de dev com Vite, ou build estático). A comunicação já usa JSON — sem mudanças no backend. Exige configuração de CORS no Flask.

**Veredito:** Solução mais robusta para o longo prazo, mas representa custo de migração e aprendizado elevado para um projeto acadêmico em andamento.

---

### Vue.js

Vue é um framework JavaScript progressivo. Pode ser adotado incrementalmente: começa como biblioteca simples e evolui para SPA completa conforme a necessidade.

**Pontos fortes:**

- Curva de aprendizado menor que React: template syntax intuitiva, Options API familiar para quem vem de HTML/JS
- Pode ser incluído via CDN sem bundler, mantendo compatibilidade com o modelo atual de arquivos estáticos
- Componentização eficiente com Single File Components (`.vue`)
- `v-model`, diretivas e reatividade reduzem código boilerplate
- Excelente documentação em português
- Ecossistema bem estabelecido (Vue Router, Pinia para estado)

**Pontos fracos:**

- Ecossistema menor que React (menos bibliotecas de terceiros)
- Adoção empresarial mais baixa no Brasil (menos vagas, menos referências locais)
- Modo progressivo via CDN não escala bem para projetos maiores
- Transição de Options API para Composition API pode causar inconsistência no código

**Compatibilidade com a arquitetura atual:**

Vue pode ser inserido progressivamente via CDN nas páginas existentes, sem reescrita imediata. Para a Release 2, a migração para SPA com Vite seria o caminho natural. Comunicação com Flask via Fetch permanece inalterada.

**Veredito:** Melhor custo-benefício entre os frameworks SPA. A adoção progressiva via CDN permite começar sem abandonar o modelo atual.

---

### Svelte

Svelte é um compilador que transforma componentes em JavaScript puro durante o build. Não existe virtual DOM em runtime.

**Pontos fortes:**

- Bundle resultante é muito menor que React ou Vue
- Sintaxe simples e próxima de HTML/CSS/JS padrão
- Reatividade nativa sem boilerplate (`$:` para computados)
- Performance excelente: sem overhead de framework em runtime

**Pontos fracos:**

- Ecossistema muito menor (menos bibliotecas, menos componentes prontos)
- Pouquíssima adoção em projetos institucionais brasileiros
- Curva de aprendizado diferente: o modelo mental de compilador pode ser confuso
- Poucos exemplos de integração com Flask
- Comunidade pequena comparada a React e Vue

**Compatibilidade com a arquitetura atual:**

Exige bundler obrigatório. Migração total das telas existentes necessária. Comunicação com Flask sem alterações.

**Veredito:** Tecnicamente interessante, mas com ecossistema insuficiente para as necessidades de dashboards e gráficos do LegisKids. Risco elevado para projeto acadêmico.

---

## 2. Bibliotecas de Enhancement (sem SPA)

### Alpine.js

Alpine é uma biblioteca mínima (~7KB) para adicionar reatividade diretamente no HTML via atributos `x-data`, `x-bind`, `x-on`. É frequentemente descrita como "jQuery moderno" ou "Tailwind para JavaScript".

**Pontos fortes:**

- Não exige bundler, funciona via CDN em qualquer arquivo HTML
- Compatível direto com o modelo atual (HTML + JS separados)
- Curva de aprendizado muito baixa — aprende-se em horas
- Reatividade declarativa no HTML reduz manipulação manual de DOM
- Tamanho mínimo: praticamente zero impacto no desempenho
- Funciona perfeitamente com Flask servindo páginas HTML

**Pontos fracos:**

- Não é adequado para interfaces complexas com estado compartilhado entre páginas
- Sem componentização real (não há reutilização de templates)
- Ecossistema muito pequeno
- Dashboards com gráficos complexos exigem JS externo de qualquer forma

**Compatibilidade com a arquitetura atual:**

Compatibilidade total. Pode ser adicionado ao HTML existente linha a linha, sem refatoração. Não altera o backend nem o modelo de comunicação.

**Veredito:** Ótimo para Release 1 — reduz manipulação de DOM manual sem introduzir complexidade. Insuficiente para o dashboard interativo da Release 2.

---

### HTMX

HTMX é uma biblioteca que permite ao HTML fazer requisições HTTP diretamente via atributos (`hx-get`, `hx-post`, `hx-target`). A resposta do servidor é HTML, não JSON.

**Pontos fortes:**

- Zero JavaScript necessário para interações simples
- Curva de aprendizado mínima
- Filosofia "hipermídia" reduz código frontend drasticamente

**Pontos fracos:**

- **Incompatível com a arquitetura atual**: exige que o Flask retorne fragmentos HTML, não JSON
- Mudaria fundamentalmente o contrato entre frontend e backend (US02 define explicitamente que o frontend nunca acessa a API externa, e que o backend retorna JSON)
- Dificulta o desacoplamento entre frontend e backend
- Gráficos interativos da Release 2 exigem JavaScript de qualquer forma

**Compatibilidade com a arquitetura atual:**

Baixa. Adotar HTMX exigiria que o Flask gerasse HTML nos endpoints, quebrando o modelo de API REST com JSON já estabelecido.

**Veredito:** Não recomendado. Conflita com a arquitetura REST definida nas specs do projeto.

---

## 3. Frameworks CSS

### Tailwind CSS

Framework utility-first: classes atômicas aplicadas diretamente no HTML (`flex`, `p-4`, `text-blue-600`). Não há componentes pré-prontos — a composição é manual.

**Pontos fortes:**

- Compatível com qualquer stack, sem dependência de framework JS
- Design system consistente via configuração (`tailwind.config.js`)
- Purging automático garante CSS final mínimo
- Ótimo para manter identidade visual personalizada (sem "look padrão de framework")

**Pontos fracos:**

- Exige PostCSS e bundler para modo de purge em produção (sem bundler, o CDN gera ~3MB de CSS)
- HTML com muitas classes pode ficar verboso
- Curva de aprendizado para memorizar as classes utilitárias
- O CSS do LegisKids já usa variáveis CSS bem estruturadas — migrar seria reescrita completa

**Compatibilidade com a arquitetura atual:**

O projeto já tem um design system próprio com variáveis CSS (`--primary`, `--bg`, etc.) e classes semânticas bem definidas. Adotar Tailwind implicaria reescrever todos os estilos existentes.

**Veredito:** Tecnicamente sólido, mas impraticável adotar agora. A base CSS atual é bem organizada e substituí-la seria desperdício. Considerar apenas em reescrita futura.

---

### Bootstrap

Framework CSS com componentes prontos (grid, navbar, modal, cards, botões).

**Pontos fortes:**

- Componentes prontos aceleram o desenvolvimento
- Documentação extensa e comunidade enorme
- Grid system responsivo robusto

**Pontos fracos:**

- "Look Bootstrap" genérico — conflita com identidade visual personalizada do LegisKids (Figma, paleta própria, fontes Cinzel/Inter)
- Bundle pesado (CSS + JS = ~200KB)
- Customização profunda exige sobrescrever muitos estilos
- O frontend atual já tem responsividade e componentes visuais definidos

**Compatibilidade com a arquitetura atual:**

Tecnicamente compatível, mas conflita com a identidade visual já estabelecida.

**Veredito:** Não recomendado. A identidade visual do projeto é uma restrição explícita nas specs — Bootstrap interfere diretamente nela.

---

## 4. Bibliotecas de Visualização de Dados

Esta categoria é crítica para o LegisKids: a Release 2 prevê gráficos de volume por subtema, evolução temporal, ranking de parlamentares e detecção de temas emergentes (US11, US12, US14).

### Chart.js

Biblioteca de gráficos simples e leve (~200KB), baseada em Canvas HTML5.

**Pontos fortes:**

- API simples: poucas linhas para criar um gráfico funcional
- Compatível com JavaScript puro, sem dependência de framework
- Tipos de gráfico suficientes para o LegisKids: linha, barra, pizza, rosca, radar
- Animações nativas suaves
- Boa documentação com exemplos claros
- Bundle leve
- Comunidade ativa e madura (mais de 63k stars no GitHub)

**Pontos fracos:**

- Customização avançada é verbosa
- Não suporta gráficos muito complexos (mapas, grafos de rede)
- Canvas não é tão acessível quanto SVG para leitores de tela

**Compatibilidade com a arquitetura atual:**

Total. Inclui-se via CDN no HTML, chama-se via JavaScript puro, alimenta-se com dados vindos do Fetch. Nenhuma dependência adicional.

```javascript
// Exemplo de integração com Fetch API
fetch('/api/proposicoes/por-subtema')
  .then(r => r.json())
  .then(data => {
    new Chart(document.getElementById('chartSubtema'), {
      type: 'bar',
      data: { labels: data.subtemas, datasets: [{ data: data.totais }] }
    });
  });
```

**Veredito:** **Recomendado**. Solução ideal para os gráficos da Release 2.

---

### D3.js

Biblioteca de visualização baseada em SVG com controle total sobre cada elemento gráfico.

**Pontos fortes:**

- Controle absoluto sobre visualizações
- Suporta qualquer tipo de gráfico imaginável
- Baseado em SVG (melhor acessibilidade)
- Usado em jornalismo de dados e aplicações científicas

**Pontos fracos:**

- Curva de aprendizado muito alta — D3 não é um "plugin de gráficos", é uma biblioteca de transformação de dados
- Código extenso para gráficos simples
- Bundle pesado (~500KB)
- Documentação densa e exemplos complexos
- Requer entendimento de SVG, scales, axes, transitions

**Compatibilidade com a arquitetura atual:**

Compatível tecnicamente, mas desproporcional para as necessidades do projeto.

**Veredito:** Não recomendado para esta fase. O overhead de aprendizado e implementação supera os benefícios para os gráficos definidos nas specs.

---

### ApexCharts

Biblioteca de gráficos baseada em SVG com API moderna e visual polido.

**Pontos fortes:**

- Gráficos com visual mais refinado que Chart.js
- Baseado em SVG (melhor acessibilidade e escalabilidade)
- API declarativa simples (objeto de configuração)
- Suporte nativo a tooltips interativos, zoom e pan
- Compatível com JavaScript puro (não precisa de React)
- Responsivo por padrão

**Pontos fracos:**

- Bundle ligeiramente maior que Chart.js (~500KB)
- Comunidade menor que Chart.js
- Customização profunda pode ser verbosa

**Compatibilidade com a arquitetura atual:**

Total. Mesma abordagem do Chart.js — via CDN, alimentado por Fetch.

**Veredito:** **Alternativa sólida ao Chart.js**. Preferível quando o visual dos gráficos é prioritário.

---

## 5. Bundlers e Ferramentas de Build

### Vite

Ferramenta de build moderna baseada em módulos ES nativos. Usada com React, Vue e Svelte.

**Relevância:** necessária apenas se um framework SPA for adotado. Para vanilla JS, Alpine.js ou bibliotecas via CDN, Vite não é obrigatório.

**Veredito:** Introduzir apenas na Release 2 se Vue ou React forem adotados. Não usar antes disso.

---

## Tabela Comparativa

| Tecnologia | Tipo | Curva de Aprend. | Compat. Flask | Compat. Atual | Desempenho | Escal. | Rec. Release 1 | Rec. Release 2 |
|---|---|---|---|---|---|---|---|---|
| **React** | Framework SPA | Alta | Total | Baixa (reescrita) | Alta | Alta | Não | Possível |
| **Vue.js** | Framework SPA | Média | Total | Média (progressivo) | Alta | Alta | Via CDN | Sim |
| **Svelte** | Compilador | Média | Total | Baixa (reescrita) | Excelente | Média | Não | Não |
| **Alpine.js** | Enhancement | Baixíssima | Total | Total | Excelente | Baixa | Sim | Parcial |
| **HTMX** | Enhancement | Baixa | Baixa | Muito Baixa | Alta | Média | Não | Não |
| **Tailwind CSS** | CSS | Média | Total | Baixa (reescrita CSS) | Alta | Alta | Não | Não |
| **Bootstrap** | CSS | Baixa | Total | Média | Média | Média | Não | Não |
| **Chart.js** | Gráficos | Baixa | Total | Total | Alta | Alta | — | Sim |
| **ApexCharts** | Gráficos | Baixa | Total | Total | Alta | Alta | — | Sim |
| **D3.js** | Gráficos | Muito Alta | Total | Total | Alta | Alta | — | Não |

---

## Recomendação

As demandas da Release 2 (dashboards rearranjeáveis, gráficos interativos, estado de usuário autenticado, histórico de buscas) superam o que o vanilla JS mantém de forma organizada.

**Recomenda-se:**

1. **Vue.js** como framework SPA, com migração progressiva das páginas existentes
2. **Vite** como bundler (configuração padrão do Vue)
3. **Chart.js** para todos os gráficos (barras, linhas, pizza) — simples de integrar, leve e suficiente para as specs
4. Manter a **identidade visual atual** (variáveis CSS, fontes, paleta) dentro dos componentes Vue — sem adotar Tailwind ou Bootstrap
5. Manter Flask como **API REST pura** — sem mudanças na camada de comunicação

**Justificativas para Vue.js sobre React:**

- Curva de aprendizado mais suave para uma equipe que está dominando JS puro
- Modo progressivo permite migrar tela por tela sem reescrita total
- A Options API do Vue é mais próxima da estrutura mental de HTML/CSS/JS que o time já usa
- Documentação em português de alta qualidade

**Justificativas para Chart.js sobre D3.js:**

- Os gráficos especificados (volume por subtema, evolução temporal, ranking) são gráficos convencionais — não há necessidade das capacidades avançadas do D3
- Chart.js reduz o tempo de implementação de dias para horas
- Integração com Fetch API é trivial e direta

---

## Plano de Adoção Gradual

```
Release 2
  └── Vue.js SPA (migração progressiva)
      ├── Vue Router (roteamento entre páginas)
      ├── Pinia (estado: usuário autenticado, filtros, histórico)
      ├── Chart.js (gráficos do dashboard)
      └── Fetch API (sem mudanças)
```

---

## Conclusão

A análise demonstra que a adoção de qualquer framework deve ser gradual e orientada pelas demandas reais de cada release. Não há necessidade de reescrita imediata.

Para a **Release 2**, o crescimento das funcionalidades justifica a adoção de **Vue.js** como framework e **Chart.js** como biblioteca de gráficos — ambos compatíveis com o backend Flask e com o modelo de comunicação via Fetch API já estabelecido.

A identidade visual definida no Figma deve ser preservada em qualquer cenário, sendo este um critério que elimina Bootstrap e Tailwind como opções viáveis no contexto atual.