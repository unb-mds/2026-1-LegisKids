## Context

O backend hoje (`GET /api/proposicoes/<id>`) retorna `proposicao` (id, sigla_tipo, numero, ano, ementa, data_apresentacao, descricao_situacao/status, sigla_partido, partido{sigla,nome}, categorias/subtemas) e `tramitacoes` (lista com data, descrição, órgão). Não existem endpoints ou colunas para: nome do autor (confirmado — `nome_autor` é sempre `null` no serializer), objetivos do projeto, documentos/anexos, indicadores de análise (relevância/impacto/apoio popular), projetos relacionados, notificações ou preferências de conta.

O spec visual `dashboard-projeto-detalhado/spec.json` foi desenhado para uma versão 100% mock (vanilla HTML/CSS/JS) e assume todos esses dados presentes. Portar isso para o Vue atual, que já é orientado a dados reais da API, exige decidir o que fica com dado real, o que fica com estado vazio explícito, e o que é adiado.

## Goals / Non-Goals

**Goals:**
- `DetalheView.vue` visualmente alinhado ao spec (paleta navy, top bar, badges, abas, cards, sidebar com timeline) sem regressão nos dados reais já exibidos hoje (autor/partido/ementa/tramitação/link do documento).
- Seções do spec sem dado real da API (objetivos, documentos, indicadores, projetos relacionados, comentários) exibem estado vazio explícito e sóbrio (reaproveitando `.empty-state` já existente em `main.css`) — nunca número ou texto inventado.
- `DashboardView.vue` ganha banner de alerta, busca rápida e ações rápidas do spec original, mantendo intactos os cards de estatística reais e os 3 gráficos Chart.js.
- Navbar ganha ícones de Configurações/Notificações e as rotas correspondentes existem, com páginas placeholder claras de que o conteúdo ainda não foi implementado.

**Non-Goals:**
- Não implementar backend novo (autores, documentos, indicadores, notificações reais, preferências de conta) — fica para changes futuras quando houver requisitos definidos (roadmap R2).
- Não implementar autenticação — o botão "Salvar" (favoritar) do top bar fica visualmente presente mas não funcional (mesmo tratamento de "em construção").
- Não remover ou alterar `GraficoSubtemas`, `GraficoStatus`, `GraficoTemporal` nem a integração com `/api/estatisticas`.
- Não portar a seção "Biblioteca Legislativa" do spec original para o Vue (removida por pedido explícito do usuário).

## Decisions

- **CSS scoped com tokens locais, sem tocar `main.css`**: `DetalheView.vue` usa `<style scoped>` com um bloco de custom properties (`--d-primary: #2B3FBF`, `--d-bg: #DDE3EE`, etc.) declarado no seletor raiz do componente (`.detalhe-page`), replicando a estratégia já usada na versão vanilla (`--d-*` escopado). As demais páginas continuam usando os tokens globais (`--primary: #2563EB`) sem alteração — evita quebrar consistência visual das outras telas.
- **Abas com placeholder para conteúdo não disponível**: as 5 abas do spec (Visão geral, Tramitação, Análise, Documentos, Comentários) existem visualmente. "Visão geral" e "Tramitação" mostram dado real (ementa/metadados e timeline de tramitação, respectivamente). "Análise", "Documentos" e "Comentários" renderizam `.empty-state` com texto explicando que o recurso ainda não está disponível. Alternativa descartada: omitir as 3 abas sem dado — rejeitada porque o pedido do usuário é "se parecer com a descrição visual", e esconder as abas foge da fidelidade visual pedida.
- **Sidebar "Status da tramitação"**: timeline construída a partir de `tramitacoes` real (mesmo dado já usado hoje), estilizada como no spec (nós coloridos, linha conectora). Sem tramitações, mostra `.empty-state`.
- **Sidebar "Análise e indicadores"**: sem dado real (relevância/impacto/apoio popular não existem no backend) → card com `.empty-state` no lugar das barras, nunca valores fabricados.
- **Card "Sobre o projeto"**: usa `ementa` real; o botão "Ver mais/Ver menos" do spec é mantido (expand/collapse), já que é comportamento puramente visual sem depender de dado adicional.
- **Card "Informações pessoais"**: grid do spec populado com os campos reais disponíveis (autor — hoje sempre "Não informado", partido, data de apresentação, situação atual); campos sem correspondência no backend (urgência, casa legislativa, regime de tramitação) exibem "Não informado" em vez de sumir do grid, mantendo a estrutura visual do spec.
- **Cards "Objetivos", "Documentos e anexos", "Projetos relacionados"**: sem dado real → cada um vira `.empty-state` com mensagem específica (ex: "Nenhum documento disponível para esta proposição"). Exceção: o link "Ver documento oficial" já existente hoje (`url_documento`/`url`, quando presente) é reaproveitado dentro do card de documentos como um item de lista, em vez de duplicar como botão solto — mantém o dado real visível sem inventar uma lista de PDFs.
- **Top bar "Compartilhar"**: implementado de fato usando a Web Share API (`navigator.share`) com fallback para copiar o link (`navigator.clipboard.writeText`) — não depende de backend, é só interação de browser, então não se enquadra como "funcionalidade não implementada".
- **Top bar "Salvar"**: sem autenticação implementada, o botão fica visualmente presente (ícone bookmark) mas ao clicar mostra uma dica não-bloqueante (ex: tooltip/alert simples "Disponível em breve") — mesmo padrão do Non-Goal de auth.
- **Dashboard: banner de alerta e ações rápidas**: usam texto estático/institucional do spec (ex: "Configurar Alertas", "Análises e Relatórios", "Participação Pública") como ações de navegação (linkam para rotas existentes ou futuras), não como dados dinâmicos — são elementos de navegação/CTA, não métricas, então não violam a regra de "não inventar dado".
- **Dashboard: busca rápida**: campo de busca que, ao submeter, navega para `/busca?q=<termo>` reaproveitando a `BuscaView` e sua querystring já existente — não duplica lógica de busca.
- **Biblioteca Legislativa removida**: nenhuma referência a essa seção é portada para `DashboardView.vue`.
- **Páginas de Configurações e Notificações como placeholder explícito**: `ConfiguracoesView.vue` e `NotificacoesView.vue` usam o padrão visual `.empty-state`/card institucional com título da página e mensagem "Em construção — funcionalidade prevista para uma próxima etapa do projeto", evitando simular preferências ou notificações falsas.
- **Ícones de navbar**: dois novos botões/links (engrenagem para Configurações, sino para Notificações) ao lado direito da Navbar, com `aria-label` e navegação via `RouterLink`, seguindo o padrão de acessibilidade já usado nos links existentes (US17).

## Risks / Trade-offs

- [Risco] Muitas seções em estado vazio podem passar impressão de página "incompleta" → Mitigação: `.empty-state` já é um padrão visual estabelecido no design system (usado em outras telas), então o efeito é consistente, não parece bug.
- [Risco] `navigator.share`/`navigator.clipboard` não funcionam em todos os navegadores/contextos (exigem HTTPS ou browsers específicos) → Mitigação: fallback encadeado (share → clipboard → mensagem manual "copie o link da barra de endereço"), sem quebrar a página se ambas APIs faltarem.
- [Risco] Retrabalho futuro quando objetivos/documentos/indicadores/autores ganharem endpoints reais → Mitigação: estrutura de componentes/props já isolada por seção (cada card é responsável por seu próprio estado vazio), facilitando substituir só o card correspondente sem tocar no restante do layout — mesmo padrão já usado no `MOCK_PROJETO` da versão vanilla, citado no proposal original.

## Migration Plan

1. `Navbar.vue`: adicionar ícones/rotas de Configurações e Notificações.
2. `router/index.js`: registrar `/configuracoes` e `/notificacoes`.
3. Criar `ConfiguracoesView.vue` e `NotificacoesView.vue` (placeholder).
4. Reconstruir `DetalheView.vue` seguindo o spec, mantendo os dados reais já consumidos por `fetchProposicao`.
5. Ajustar `DashboardView.vue`: adicionar banner de alerta, busca rápida, ações rápidas; não incluir Biblioteca Legislativa.
6. Validar visualmente com `npm run dev` e rodar `npm run build` para garantir ausência de erros de template.

Rollback: reverter os arquivos alterados via git; nenhuma mudança de backend, banco ou API envolvida.

## Open Questions

Nenhuma — decisões acima cobrem as ambiguidades já identificadas nas perguntas de esclarecimento feitas ao usuário.
