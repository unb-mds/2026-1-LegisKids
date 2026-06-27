# CLAUDE.md — LegisKids

Projeto acadêmico desenvolvido para a disciplina de Métodos de Desenvolvimento de Software (MDS) da Universidade de Brasília (UnB), turma 2026/1.

---

## Visão Geral

O LegisKids é uma plataforma web para monitoramento, organização e análise de proposições legislativas da Câmara dos Deputados do Brasil, com foco em proteção de crianças e adolescentes no ambiente digital.

**O sistema permite:** monitoramento de projetos de lei, busca avançada de proposições, classificação automática com IA, visualização de métricas legislativas, sistema de alertas, dashboards analíticos, acompanhamento de tramitações e filtragem semântica de conteúdo.

**Temas principais:** cyberbullying, exploração sexual infantil online, proteção de dados de menores, segurança digital infantil, regulação de plataformas digitais e conteúdos nocivos para menores.

---

## Stack Oficial

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.11+ / Flask |
| Banco de dados | PostgreSQL + SQLAlchemy + psycopg |
| Frontend | Vue 3 + Vite |
| Roteamento | Vue Router 4 |
| Estado global | Pinia |
| Gráficos | Chart.js 4 |
| Requisições HTTP | Fetch API (via services) |
| IA | Google Gemini API (gemini-1.5-flash) |
| Dados Legislativos | API da Câmara dos Deputados |
| Documentação | MkDocs |
| CI/CD | GitHub Actions |

---

## Estrutura do Projeto

```
2026-1-Squad08/
├── backend/
│   └── src/
│       ├── main.py
│       ├── routes/
│       ├── services/
│       ├── models/
│       └── utils/
├── src/
│   ├── backend/                 ← Flask + SQLAlchemy
│   └── frontend/                ← Projeto Vue 3 + Vite
│       ├── index.html
│       ├── vite.config.js
│       ├── package.json
│       ├── .env.example
│       └── src/
│           ├── main.js
│           ├── App.vue
│           ├── assets/
│           │   └── main.css     ← variáveis CSS / design tokens
│           ├── router/
│           │   └── index.js
│           ├── stores/          ← Pinia
│           │   ├── busca.js
│           │   └── proposicoes.js
│           ├── services/        ← Fetch API encapsulada
│           │   ├── proposicoes.js
│           │   ├── temas.js
│           │   └── estatisticas.js
│           ├── components/
│           │   ├── charts/      ← Chart.js
│           │   ├── Navbar.vue
│           │   ├── StatusBadge.vue
│           │   ├── LoadingSpinner.vue
│           │   ├── ProposicaoCard.vue
│           │   ├── FilterBar.vue
│           │   └── Pagination.vue
│           └── views/
│               ├── DashboardView.vue
│               ├── BuscaView.vue
│               └── DetalheView.vue
├── docs/
│   ├── estudos/
│   ├── projeto/
│   ├── reunioes/
│   ├── padrao_organizacao/
│   ├── performance/
│   └── sdd/
├── openspec/
│   ├── specs/
│   └── changes/
├── scripts/
├── .github/
├── mkdocs.yml
├── requirements.txt
├── README.md
└── CLAUDE.md
```

---

## Estado Atual

**Backend:** integração com API da Câmara, filtros por palavras-chave, busca de proposições, listagem de temas, retry automático para falhas 504 e CLI interativa inicial.

**Frontend:** scaffold HTML inicial, navbar básica, estrutura visual inicial, protótipo completo no Figma e identidade visual definida.

**Documentação:** estudos técnicos, MkDocs, atas de reuniões, padrões de organização, estudos de arquitetura, banco de dados, IA, frontend e requisitos.

**DevOps:** GitHub Actions configurado com métricas automáticas e workflow de performance.

---

## Roadmap de Releases

### Release 1 — Frontend básico consumindo a API do backend

Objetivo: entregar telas funcionais que consomem os endpoints do backend via Fetch API. O backend já existe — o foco é o frontend. Sem IA, sem autenticação, sem histórico por usuário.

**Épico: Visualização Básica**
- US13 — Estatísticas resumidas: total de proposições no período, distribuição por subtema, variação vs. período anterior, data da última atualização
- US15 — Tela de detalhes: título, autor, partido, data, status, ementa completa, link para documento oficial, histórico de tramitação em linha do tempo

**Épico: Busca e Filtros**
- US08 — Busca por palavra-chave (parcial, case-insensitive), retorno em até 3s *(sem histórico por usuário — requer autenticação, vai para R2)*
- US09 — Filtros combinados por parlamentar, partido, data e subtema; filtros exibidos como tags removíveis
- US10 — Paginação configurável (10/25/50 itens)

**Épico: Usabilidade**
- US17 — Interface responsiva (320px a desktop), contraste WCAG AA, navegação por teclado

---

### Release 2 — Backend completo, IA, Autenticação e Rastreabilidade

Objetivo: completar a fundação técnica do backend, adicionar inteligência, autenticação e funcionalidades que dependem de usuário autenticado.

**Épico: Coleta de Dados e Infraestrutura**
- US01 — Coleta automática de proposições da Câmara, sem duplicatas, com registro de data/hora
- US02 — Integração com `dadosabertos.camara.leg.br/api/v2`; retry mínimo de 3 tentativas; frontend nunca consome a API externa
- US03 — Armazenamento em PostgreSQL com schema relacional; acesso exclusivo via camada de Repositories
- US-ETL — Pipeline de tratamento antes da persistência: limpeza, normalização de datas (ISO 8601), mapeamento ao schema, rejeição de registros inválidos com log; execução assíncrona
- US-LAYERS — Backend com separação rígida de camadas; módulo `backend/ai/` chamado apenas por Services
- US-TRAM — Job diário de atualização de tramitações; persiste timestamp da última execução bem-sucedida

**Épico: Autenticação**
- US19 — Login com Google OAuth 2.0; sem senha armazenada; token em cookie `httpOnly`; na primeira autenticação cria usuário com perfil `citizen`
- US20 — Redirecionamento pós-login para URL original; sessão válida por 24h; proteção CSRF e open redirect
- US21 — Persistência de sessão via refresh token com rotação; opção "lembrar por 30 dias"; logout revoga token no Google

**Épico: Classificação por IA**
- US05 — Classificação automática por subtema via NLP; score de confiança exibido; timeout de 5s por proposição salva como `pendente_classificacao`
- US06 — Múltiplos subtemas por proposição: 1 primário obrigatório + até 4 secundários; autocomplete com subtemas existentes
- US-AI-RESILIÊNCIA — Falha no módulo de IA não bloqueia o pipeline ETL; job periódico reclassifica proposições pendentes

**Épico: Indicadores e Análises**
- US08 (complemento) — Histórico das últimas 10 buscas por usuário autenticado
- US09 (complemento) — Estado dos filtros preservado na paginação; URL reflete página atual
- US11 — Gráficos interativos: volume por subtema, evolução temporal, ranking de parlamentares mais ativos
- US12 — Detecção de temas emergentes por crescimento acelerado de frequência; comparação com mesmo período do ano anterior
- US14 — Dashboard interativo com widgets rearranjeáveis, atualização dinâmica sem reload
- Relatórios exportáveis em PDF (tendências legislativas)
- Exportação de dados em CSV/JSON

**Épico: Rastreabilidade e Auditoria**
- US16 — Histórico de mudanças nas proposições: diff por campo, registro de responsável, filtrável por período/tipo/responsável
- US-HIST — Tabela `historico` com `user_id`, `proposicao_id`, `tipo_acao`, `timestamp`; usuário vê seus últimos 30 eventos; conformidade LGPD
- US-AUDIT — Payload JSON original da API armazenado imutavelmente; retenção mínima de 1 ano
- Favoritos: relação `user_id` + `proposicao_id`; notificações ao usuário quando proposição favoritada é atualizada
- Alertas automáticos para usuários (nova proposição relevante, mudança de status)

---

## Filosofia de Desenvolvimento

```
Spec → Planejamento → Tarefas → Implementação → Validação
```

Antes de implementar: entender o problema, analisar arquivos afetados, propor plano, validar escopo e implementar somente o necessário.

---

## Fluxo Obrigatório (OpenSpec + SDD)

O projeto usa o sistema **OpenSpec** para gerenciar o ciclo de vida de cada funcionalidade. Toda implementação relevante deve passar pelas etapas abaixo, nessa ordem:

| Etapa | Comando | O que faz |
|---|---|---|
| **Explorar** | `/opsx:explore` | Pensar o problema antes de propor solução. Modo de descoberta — sem implementação. |
| **Propor** | `/opsx:propose` | Gerar todos os artefatos da mudança: `proposal.md`, `design.md`, `tasks.md`. |
| **Implementar** | `/opsx:apply` | Executar as tasks geradas na proposta, marcando cada uma como concluída. |
| **Arquivar** | `/opsx:archive` | Finalizar a mudança e mover para `openspec/changes/archive/`. |

## OpenSpec Workflow

O projeto usa OpenSpec para gerenciamento de mudanças.

Fluxo padrão:

1. /opsx:explore
2. /opsx:propose
3. /opsx:apply
4. /opsx:archive

---

## Exceção: spec.json como entrada válida

Quando existir um arquivo:

openspec/changes/<change-name>/specs/<feature>/spec.json

ele deve ser considerado uma fonte oficial de especificação visual e estrutural.

Nesse caso, o agente DEVE:

1. Ler o spec.json
2. Gerar automaticamente:
   - proposal.md
   - design.md
   - tasks.md
3. Só depois iniciar implementação.

O usuário pode criar manualmente apenas o spec.json.

O agente NÃO deve exigir proposal.md/tasks.md previamente quando spec.json existir.

---

## Regra de implementação

Nenhuma implementação deve começar sem:

- spec.json
OU
- proposal.md + tasks.md

Se houver apenas spec.json, o agente deve completar automaticamente o restante do fluxo OpenSpec antes da implementação.

Os artefatos de cada mudança ficam em `openspec/changes/<nome-da-mudança>/`.

**Toda spec deve conter:** Objetivo, Contexto, Escopo, Requisitos, Critérios de aceitação, Restrições e Testes.

O agente **não deve iniciar nenhuma implementação sem que a spec da mudança exista** em `openspec/changes/<nome-da-mudança>/`.

---

## Regras do Agente

**Deve:** seguir a spec antes de implementar, preservar arquitetura existente, manter consistência visual, reutilizar componentes, criar código modular, respeitar escopo, evitar duplicação e usar nomes semânticos.

**Não deve:** alterar funcionalidades fora do escopo, reescrever arquitetura sem necessidade, criar sistemas paralelos, modificar identidade visual sem solicitação, adicionar dependências desnecessárias ou remover código sem justificar.

---

## Diretrizes Técnicas

**CSS:** evitar inline, usar classes semânticas, variáveis CSS, sem duplicação, manter responsividade.

**JavaScript:** separar lógica da interface, usar módulos organizados, Fetch API, evitar dependências desnecessárias.

**Backend:** separar services/routes/models, validar entradas, tratar erros de API, evitar acoplamento.

**IA:** considerar custo de chamadas, modularidade, possibilidade de fallback e facilidade de troca futura do modelo.

**Banco:** evitar schemas excessivamente complexos, manter modelagem relacional limpa e consistência dos dados. O schema inclui a tabela `categorias` — uma proposição pode estar associada a uma ou várias categorias (relação muitos-para-muitos via tabela intermediária `proposicao_categorias`).

---

## Frontend e Figma

A implementação visual deve seguir o protótipo do Figma respeitando paleta de cores, estrutura dos dashboards, espaçamentos, hierarquia visual, cards, navbar e componentes institucionais.

O frontend deve parecer moderno, institucional, organizado, confiável e acessível.

---

## Convenções

**Branches:** `feature/`, `fix/`, `docs/`, `refactor/`, `hotfix/`

**Commits:** `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`

---

## Variáveis de Ambiente

```env
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:<senha>@localhost:5432/legiskids
GOOGLE_API_KEY=<chave_gemini>
```

---

## Execução Local

**Backend:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
flask run
```

**Frontend:**
```bash
cd src/frontend
cp .env.example .env          # configurar VITE_API_BASE_URL se necessário
npm install
npm run dev                    # http://localhost:5173
```

**Build de produção do frontend:**
```bash
cd src/frontend
npm run build                  # gera src/frontend/dist/
```

---

## Objetivo Final

Transformar o LegisKids em uma plataforma funcional para acompanhamento legislativo focado em proteção infantil digital, utilizando IA e visualização de dados para facilitar o acesso à informação pública.

---

> Não implemente primeiro. Entenda primeiro. Specs guiam o código. Arquitetura guia o sistema.