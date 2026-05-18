## Context

O repositório `2026-1-Squad08` é um projeto acadêmico da disciplina MDS/UnB. Atualmente não existe nenhuma automação para acompanhar a participação individual dos membros. O grupo usa GitHub para colaboração (commits, issues, PRs). O relatório precisa funcionar sem segredos adicionais, apenas com `GITHUB_TOKEN`, e os artefatos gerados devem ser versionados no próprio repositório para facilitar o acesso via GitHub Pages ou download direto.

## Goals / Non-Goals

**Goals:**
- Workflow executável manualmente (`workflow_dispatch`) que não interfere em outros fluxos (CI/CD existente)
- Script Python legível e manutenível por estudantes, sem dependências externas além da stdlib
- Mapeamento explícito de alunos via `.github/performance-students.json` para correlacionar logins GitHub com e-mails de commit
- Paginação completa da API de issues para repositórios com muitas issues
- HTML estático que abre diretamente no navegador, sem servidor
- JSON estruturado e reutilizável por dashboards futuros

**Non-Goals:**
- Avaliação automática ou ranking oficial de membros
- Integração com ferramentas externas (Jira, Notion, Slack)
- Análise de pull requests como proxy de contribuição
- Métricas de qualidade de código (linhas, complexidade)

## Decisions

### 1. Python em vez de JavaScript para o script de coleta

**Decisão:** Usar Python 3 com stdlib (`urllib`, `subprocess`, `json`, `datetime`).

**Rationale:** O projeto já tem um backend Python/Django; Python é familiar para o time. Node.js adicionaria um runtime extra sem vantagem prática. A stdlib cobre todas as necessidades (HTTP, JSON, git subprocess), evitando dependências instaladas via pip/npm.

**Alternativas consideradas:**
- **Node.js/TypeScript**: exigiria `npm install` no workflow e seria menos familiar para o time de backend.
- **GitHub CLI (`gh`)**: simplificaria chamadas de API, mas adicionaria dependência de versão do `gh` no runner e é menos transparente para estudantes.
- **GitHub Actions de terceiros**: introduzem supply-chain risk e são caixas-pretas.

### 2. Commitar artefatos gerados no repositório

**Decisão:** O workflow usa `git commit && git push` para salvar `metrics.json` e `index.html` em `docs/performance/`.

**Rationale:** Permite acesso imediato via GitHub Pages e histórico versionado das métricas. Alternativas (GitHub Pages deploy action, artifacts temporários) exigem configuração adicional ou perdem histórico.

**Alternativas consideradas:**
- **Upload de artefato temporário**: artefatos expiram em 90 dias, sem histórico permanente.
- **GitHub Pages via branch `gh-pages`**: mais complexo de configurar e manter.

### 3. Arquivo de configuração de alunos em `.github/performance-students.json`

**Decisão:** Mapear alunos com `name`, `github` (login) e `emails` (lista de e-mails usados em commits).

**Rationale:** O `git log` registra autores por e-mail/nome, enquanto a API de issues retorna o login do GitHub. Sem esse mapeamento, não é possível consolidar métricas de um mesmo aluno. O arquivo é versionado e fácil de editar manualmente.

### 4. Chart.js via CDN para gráficos

**Decisão:** Carregar Chart.js de CDN no HTML gerado.

**Rationale:** Zero configuração de build. O HTML é um arquivo único e estático. Chart.js é amplamente documentado e familiar.

**Alternativas consideradas:**
- **D3.js**: mais poderoso, porém complexidade desnecessária para gráficos de barras/linhas simples.
- **Gráficos SVG manuais**: muito verboso para manutenção por estudantes.

### 5. Permissões mínimas no workflow

**Decisão:** Declarar explicitamente `contents: write` e `issues: read` no workflow.

**Rationale:** Segue o princípio de menor privilégio. `contents: write` é necessário apenas para commitar os artefatos. `issues: read` para consultar a API. Nenhum outro escopo é necessário.

## Risks / Trade-offs

- **Runner sem acesso à rede para CDN** → O HTML não renderizará gráficos offline. Mitigação: documentar que o HTML requer internet para Chart.js.
- **git push falha em branch protegida** → Se `main` tiver proteções que exigem PR. Mitigação: o workflow pode ser configurado para commitar em branch separada ou usar `stefanzweifel/git-auto-commit-action` com bypass de branch protection (documentar como configurar).
- **API rate limit do GITHUB_TOKEN** → 5000 requisições/hora; para repositórios pequenos, sem risco. Mitigação: paginação eficiente e uma única execução manual por vez.
- **Aluno com múltiplos e-mails não cadastrados** → Commits não atribuídos aparecem como "unknown". Mitigação: documentar que o `.github/performance-students.json` deve ser mantido atualizado pelo grupo.

## Migration Plan

1. Adicionar `.github/performance-students.json` com dados dos membros do grupo
2. Adicionar `scripts/generate_performance_report.py`
3. Adicionar `.github/workflows/performance-report.yml`
4. Criar estrutura `docs/performance/` (pode estar vazia inicialmente)
5. Executar o workflow manualmente via GitHub Actions para validar
6. Opcionalmente habilitar GitHub Pages apontando para `docs/`

Rollback: remover os 3 arquivos adicionados; nenhum código existente é alterado.
