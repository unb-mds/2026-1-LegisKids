## Context

O repositório já possui um relatório em `docs/performance/index.html` gerado por `scripts/generate_performance_report.py`, com dados vindos de `git log` e da API de issues do GitHub. O HTML atual é estático, usa Chart.js via CDN e mostra totais por aluno, mas ainda não oferece filtros, timelines, tabelas detalhadas nem métricas de pull requests/reviews.

O público principal é o próprio Squad08, que precisa acompanhar produtividade acadêmica de forma objetiva, rápida e auditável. A solução deve continuar simples de executar no GitHub Actions, sem servidor, sem segredos adicionais e sem um pipeline frontend.

## Goals / Non-Goals

**Goals:**
- Transformar o relatório em um dashboard estático interativo, eficiente para leitura e comparação.
- Incluir métricas relevantes de commits, issues, pull requests, reviews, estados e atividade recente.
- Permitir filtros por aluno, período e tipo de métrica sem recarregar a página.
- Disponibilizar gráficos e tabelas que ajudem a responder: quem contribuiu, quando contribuiu, em que tipo de atividade e quais itens estão pendentes.
- Manter o `metrics.json` como fonte estruturada e reutilizável para futuras melhorias.
- Continuar funcionando por abertura direta do HTML ou via GitHub Pages.

**Non-Goals:**
- Criar avaliação automática de desempenho individual ou ranking oficial do grupo.
- Medir qualidade de código, complexidade, cobertura de testes ou linhas alteradas.
- Integrar ferramentas externas além do GitHub.
- Criar aplicação SPA com build, backend ou autenticação.
- Exibir dados privados que não estejam disponíveis ao workflow com `GITHUB_TOKEN`.

## Decisions

### 1. Coleta no Python, visualização no HTML

**Decisão:** O script Python deve coletar e normalizar todos os dados do GitHub, e o HTML deve apenas renderizar, filtrar e agregar localmente o JSON gerado.

**Rationale:** Mantém o dashboard auditável e simples para estudantes. O HTML não precisa chamar a API do GitHub, evitando token no navegador, CORS e dependência de rede para dados.

**Alternativas consideradas:**
- **Chamar GitHub API diretamente no navegador:** descartado por exigir token público ou sofrer rate limit anônimo.
- **Criar backend para métricas:** descartado por adicionar operação e hospedagem sem necessidade.

### 2. `metrics.json` com dados agregados e eventos detalhados

**Decisão:** O JSON deve conter totais por aluno, timelines consolidadas e listas detalhadas de commits, issues e pull requests com campos mínimos para tabelas.

**Rationale:** Agregados aceleram KPIs e gráficos; eventos detalhados permitem tabelas filtráveis e validação manual dos números. Essa combinação evita recomputar tudo no navegador e mantém transparência.

**Alternativas consideradas:**
- **Somente agregados:** limitaria auditoria e tabelas detalhadas.
- **Somente eventos brutos:** deixaria o HTML mais complexo e sujeito a inconsistências.

### 3. Pull requests tratados separadamente de issues

**Decisão:** PRs devem ser coletados e exibidos como métrica própria, sem contaminar contagens de issues.

**Rationale:** A API de issues do GitHub retorna PRs junto com issues, mas eles representam fluxos diferentes. Separar melhora a leitura de produtividade: discussão, implementação, revisão e integração.

**Alternativas consideradas:**
- **Somar PRs em issues:** descartado porque distorce métricas de organização e comunicação.

### 4. Interatividade sem framework

**Decisão:** Implementar filtros, ordenação de tabelas, alternância de gráficos e busca textual com JavaScript puro e Chart.js.

**Rationale:** O projeto não precisa de build frontend para um relatório estático. JavaScript puro reduz dependências, facilita manutenção e funciona no arquivo gerado.

**Alternativas consideradas:**
- **React/Vite:** descartado por exigir build, dependências e organização adicional para uma página gerada.
- **D3.js:** poderoso, mas complexo demais para gráficos comuns.

### 5. Métricas relevantes e não punitivas

**Decisão:** Exibir dados objetivos como commits, issues abertas/fechadas, PRs abertos/mergeados/fechados, reviews, timelines, atividade recente e itens pendentes, com texto indicando que são indicadores auxiliares.

**Rationale:** Métricas de produtividade podem ser mal interpretadas se virarem ranking absoluto. O dashboard deve ajudar o time a enxergar trabalho e gargalos, não substituir avaliação qualitativa.

## Risks / Trade-offs

- **GitHub API com paginação ou limites de taxa** -> Implementar paginação de 100 itens por página e evitar chamadas desnecessárias; para o tamanho do repositório, `GITHUB_TOKEN` é suficiente.
- **Dados incompletos por e-mails não mapeados** -> Manter seção de "não atribuídos" e orientar atualização de `.github/performance-students.json`.
- **HTML grande por embutir dados detalhados** -> Limitar campos dos eventos ao necessário para visualização e auditoria.
- **Chart.js indisponível offline** -> Manter tabelas e KPIs renderizáveis mesmo se gráficos falharem; documentar dependência de internet para CDN.
- **Branch protegida impedindo commit automático** -> Manter o workflow atual como geração manual; se necessário, publicar em branch/PR separado em melhoria futura.

## Migration Plan

1. Expandir `scripts/generate_performance_report.py` para coletar PRs, reviews e campos adicionais de issues.
2. Atualizar o schema de `metrics.json` mantendo compatibilidade com campos atuais sempre que possível.
3. Recriar `docs/performance/index.html` com filtros, KPIs, gráficos e tabelas detalhadas.
4. Executar o gerador localmente para validar que HTML e JSON são produzidos sem token exposto.
5. Executar o workflow manualmente no GitHub Actions para validar dados reais.

Rollback: restaurar a versão anterior de `scripts/generate_performance_report.py`, `docs/performance/metrics.json` e `docs/performance/index.html`.

## Open Questions

- O squad quer considerar merge commits como commits produtivos comuns ou separá-los visualmente?
- Reviews devem ser atribuídas ao autor da review ou também contar comentários em PRs feitos fora de review formal?
