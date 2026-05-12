# Backlog de Produto — Sistema de Proposições Legislativas

**Versão 5.0 — Final**

Incorpora: revisão de qualidade (v2) · Estudo de Fluxo de Dados (v3) · Estudo de Login (v4) · Diagrama de Arquitetura v2 (v5)

Decisão registrada: escopo limitado à Câmara dos Deputados — Senado removido em 03/05/2026

Total: 10 épicos · 34 user stories · 95+ critérios de aceitação

---

## Legenda

- Critérios **sem marcação** — originais do backlog
- Critérios `[NOVO]` — adicionados na revisão de qualidade (v2)
- Critérios `[CORREÇÃO]` — corrigidos após conformidade com o Estudo de Fluxo de Dados (v3)
- Critérios `[CORREÇÃO-LOGIN]` — corrigidos após conformidade com o Estudo de Login — decisão: Google OAuth 2.0 (v4)
- Critérios `[CORREÇÃO-ARQ]` — corrigidos após conformidade com o Diagrama de Arquitetura v2 (v5)
- User stories `[NOVA US]` — criadas após relatórios de conformidade

---

## Decisões de arquitetura consolidadas

**Stack definida (Arquitetura v2):**

- Frontend: HTML + CSS + JavaScript + Fetch
- Backend: Python + Flask
- Autenticação: Google OAuth 2.0
- IA: spaCy / transformers (decisão pendente)
- Banco: PostgreSQL + SQLAlchemy + psycopg

**Escopo de dados:** apenas proposições da Câmara dos Deputados do Brasil. O Senado Federal foi removido do escopo desta versão — decisão registrada em 03/05/2026.

**Princípio central:** o frontend nunca acessa a API externa diretamente. Todos os dados são preparados pelo backend antes de serem entregues ao cliente.

---

## Épico 1 — Coleta de Dados Legislativos

### US01 — Coleta automática de proposições

**Como** analista, **quero** que o sistema colete proposições legislativas de fontes oficiais, **para que** eu tenha dados atualizados automaticamente.

**Critérios de aceitação:**

- `[CORREÇÃO-ARQ]` Deve coletar dados exclusivamente da API da Câmara dos Deputados
- Deve evitar duplicação de dados por identificador único
- Deve registrar data e hora da coleta
- `[NOVO]` Deve validar a estrutura dos dados antes de armazenar
- `[NOVO]` Deve alertar o administrador em caso de falha na coleta
- `[NOVO]` Deve suportar reprocessamento manual de uma coleta falha

---

### US02 — Integração com a API da Câmara dos Deputados

**Como** sistema, **quero** integrar a API oficial da Câmara dos Deputados, **para que** os dados coletados sejam confiáveis e atualizados.

**Critérios de aceitação:**

- `[CORREÇÃO-ARQ]` Integração exclusiva com a API de Dados Abertos da Câmara (api.camara.leg.br)
- Tratamento de falhas de conexão com retry automático (mínimo 3 tentativas)
- Logs de erro com timestamp e código HTTP da falha
- `[NOVO]` Autenticação via token deve ser renovada automaticamente quando expirada
- `[NOVO]` Tempo máximo de resposta tolerado: 10s por requisição
- `[NOVO]` Versão da API consumida deve ser registrada no log de cada coleta
- `[NOVO]` O frontend nunca deve consumir a API externa diretamente — todo acesso ocorre exclusivamente no backend

---

### US03 — Armazenamento estruturado de proposições

**Como** sistema, **quero** armazenar proposições em banco de dados relacional, **para que** elas possam ser consultadas com alta performance.

**Critérios de aceitação:**

- Persistência confiável com integridade referencial
- Campos obrigatórios: título, autor, data, número, situação e casa legislativa
- Suporte a crescimento de dados sem degradação de performance
- `[CORREÇÃO]` Proposições devem ser armazenadas em PostgreSQL com schema relacional; armazenamento como JSON bruto não é permitido
- `[CORREÇÃO-ARQ]` O acesso ao banco deve ocorrer exclusivamente pela camada Repositories — nenhuma rota ou controller deve executar queries diretamente
- `[NOVO]` Deve implementar soft delete (exclusão lógica, não física)
- `[NOVO]` Deve manter histórico de versões de proposições alteradas
- `[NOVO]` Backups automáticos diários com retenção mínima de 30 dias

---

### US-ETL — Pipeline de tratamento e normalização de dados `[NOVA US]`

**Como** sistema, **quero** tratar e normalizar os dados brutos recebidos da API antes de armazená-los, **para que** as proposições sejam persistidas com consistência, qualidade e prontidão para análise e dashboards.

Esta US cobre a camada Services do backend — onde ficam as regras de negócio e o processamento dos dados, conforme definido na Arquitetura v2.

**Critérios de aceitação:**

- `[NOVO]` Dados brutos da API devem passar por etapa de limpeza antes de serem persistidos
- `[NOVO]` Campos nulos ou inconsistentes devem ser tratados com valores padrão ou descartados com log
- `[NOVO]` Datas devem ser normalizadas para o formato ISO 8601
- `[NOVO]` Campos relevantes devem ser mapeados para o schema relacional: tipo, número, ementa, autor, partido, data, situação, casa legislativa
- `[NOVO]` Proposições duplicadas (mesmo ID) devem ser identificadas e apenas atualizadas se houver mudança
- `[NOVO]` Registros que não atendam ao schema mínimo devem ser rejeitados e registrados em log com motivo
- `[NOVO]` O pipeline deve ser executado de forma assíncrona, sem bloquear outras operações
- `[NOVO]` Deve ser possível reprocessar um lote de dados brutos manualmente sem afetar dados já validados
- `[CORREÇÃO-ARQ]` O pipeline ETL deve residir na camada Services — não em routes nem em controllers

---

### US-AUDIT — Armazenamento do payload original da API `[NOVA US]`

**Como** administrador, **quero** que o JSON original retornado pela API seja armazenado junto à proposição tratada, **para que** seja possível auditar os dados de origem e reprocessar proposições no futuro sem depender da API.

**Critérios de aceitação:**

- `[NOVO]` O payload JSON original deve ser armazenado de forma imutável no momento da coleta
- `[NOVO]` O JSON original deve estar associado à proposição tratada por chave estrangeira (proposicao_id)
- `[NOVO]` Não deve ser possível editar ou excluir o JSON original via interface — apenas leitura e reprocessamento
- `[NOVO]` Deve ser possível acionar o reprocessamento de uma proposição a partir do JSON original sem nova chamada à API
- `[NOVO]` O administrador deve visualizar o JSON original na tela de detalhes administrativos da proposição
- `[NOVO]` Retenção mínima do payload original: 1 ano a partir da data de coleta
- `[NOVO]` O armazenamento do JSON original não deve impactar a performance das consultas sobre dados tratados (deve estar em tabela ou storage separado)

---

### US-TRAM — Atualização incremental de proposições via tramitação `[NOVA US]`

**Como** sistema, **quero** identificar proposições atualizadas usando o endpoint de tramitações no período, **para que** a coleta diária seja eficiente — atualizando apenas o que mudou, sem reprocessar toda a base.

A API da Câmara não fornece campo de atualização global. A tramitação é usada como proxy de mudança — pequenas inconsistências são aceitas, pois o sistema serve análise política, não auditoria jurídica.

**Critérios de aceitação:**

- `[NOVO]` O job diário deve consultar `listarProposicoesTramitadasNoPeriodo` com o intervalo desde a última execução bem-sucedida
- `[NOVO]` O sistema deve persistir o timestamp da última verificação bem-sucedida
- `[NOVO]` Para cada ID retornado, o sistema deve chamar `ObterProposicaoPorID` e atualizar os dados no banco
- `[NOVO]` Proposições não retornadas na tramitação do período não devem ser reprocessadas
- `[NOVO]` O job deve registrar: quantidade de proposições verificadas, atualizadas, com erro, e os timestamps de início e fim
- `[NOVO]` Em caso de falha parcial, o job deve continuar processando os demais IDs e registrar os erros individualmente
- `[NOVO]` A interface deve exibir aviso informando que as atualizações são baseadas em tramitações e podem não capturar alterações editoriais sem movimentação processual
- `[NOVO]` Deve ser possível forçar a recoleta completa de um ID específico manualmente pelo administrador

---

### US-LAYERS — Separação de camadas no backend `[NOVA US]`

**Como** desenvolvedor, **quero** que o backend siga rigorosamente a separação routes → controllers → services → repositories, **para que** o código seja testável, manutenível e consistente com a estrutura do projeto.

**Critérios de aceitação:**

- `[NOVO]` Nenhuma rota Flask deve conter lógica de negócio — rotas apenas recebem a requisição e delegam ao controller
- `[NOVO]` Controllers validam a entrada, chamam o service e retornam a resposta — não devem acessar o banco diretamente
- `[NOVO]` Services contêm todas as regras de negócio — não devem conhecer detalhes de HTTP (request/response)
- `[NOVO]` Repositories são os únicos responsáveis pelo acesso ao banco via SQLAlchemy — nenhuma query deve existir fora dessa camada
- `[NOVO]` O módulo de IA (`backend/ai/`) deve ser chamado exclusivamente pela camada Services
- `[NOVO]` A estrutura de pastas deve seguir: `backend/auth/`, `routes/`, `controllers/`, `services/`, `repositories/`, `ai/`, `models/`, `config/`

---

### US-AI-RESILIÊNCIA — Tolerância a falhas no módulo de IA `[NOVA US]`

**Como** sistema, **quero** que uma falha no módulo de classificação por IA não bloqueie o pipeline ETL, **para que** proposições continuem sendo coletadas e armazenadas mesmo quando a IA estiver indisponível.

**Critérios de aceitação:**

- `[NOVO]` Proposições que não puderam ser classificadas devem ser salvas com status `pendente_classificacao`
- `[NOVO]` Um job de reclassificação deve processar periodicamente as proposições com status `pendente_classificacao`
- `[NOVO]` Falhas isoladas no módulo de IA devem gerar log e alerta ao administrador, sem interromper o processamento dos demais itens do lote
- `[NOVO]` Tempo máximo de espera pela classificação por proposição: 10s — após esse limite, salvar como pendente
- `[NOVO]` A interface deve exibir indicação visual quando uma proposição ainda não foi classificada

---

### US-README — Documentação de setup para desenvolvedores `[NOVA US]`

**Como** desenvolvedor novo no projeto, **quero** um README com instruções claras de instalação e configuração, **para que** eu consiga rodar o projeto localmente sem depender de outra pessoa.

**Critérios de aceitação:**

- `[NOVO]` Documentar todas as dependências: Python (versão mínima), Flask, PostgreSQL, psycopg, SQLAlchemy
- `[NOVO]` Listar todas as variáveis de ambiente obrigatórias com descrição e exemplo de valor
- `[NOVO]` Incluir passo a passo para criação e migração do banco de dados local
- `[NOVO]` Documentar como configurar as credenciais do Google OAuth para ambiente de desenvolvimento
- `[NOVO]` Documentar como acionar o ETL manualmente para popular o banco em ambiente local
- `[NOVO]` Incluir descrição das camadas da arquitetura e onde cada tipo de código deve residir

---

## Épico 2 — Classificação de Proposições

### US05 — Classificação automática por subtema

**Como** analista, **quero** que o sistema classifique proposições automaticamente, **para que** eu possa analisar rapidamente grandes volumes.

**Critérios de aceitação:**

- Uso de modelo de NLP (spaCy ou transformers — decisão técnica pendente) treinado na base legislativa
- Classificação em pelo menos um subtema por proposição
- Suporte a múltiplos subtemas simultaneamente
- `[NOVO]` Exibir score de confiança da classificação
- `[NOVO]` Proposições com baixa confiança devem ser sinalizadas para revisão manual
- `[NOVO]` Modelo deve ser retreinável com novas correções manuais
- `[NOVO]` Tempo máximo de classificação: 5s por proposição (após esse limite, salvar como `pendente_classificacao`)
- `[CORREÇÃO-ARQ]` A classificação deve ser executada pelo módulo `backend/ai/` e chamada exclusivamente pela camada Services

---

### US06 — Múltiplos subtemas por proposição

**Como** analista, **quero** associar múltiplos subtemas a uma proposição, **para que** a classificação seja mais fiel ao conteúdo.

**Critérios de aceitação:**

- Permitir seleção de múltiplos subtemas em uma única proposição
- Exibição clara dos subtemas associados na listagem e no detalhe
- `[NOVO]` Deve haver um subtema principal (obrigatório) e subtemas secundários (opcionais)
- `[NOVO]` Limite máximo de 5 subtemas por proposição
- `[NOVO]` Autocomplete deve sugerir subtemas existentes ao digitar

---

## Épico 3 — Busca e Filtros

### US08 — Busca por palavra-chave

**Como** usuário, **quero** buscar proposições por palavra-chave, **para que** eu encontre conteúdos relevantes rapidamente.

**Critérios de aceitação:**

- Busca parcial e sem distinção de maiúsculas/minúsculas
- Ordenação por data ou por relevância (TF-IDF/score)
- `[NOVO]` Destacar o termo buscado nos resultados (highlight)
- `[NOVO]` Busca deve retornar resultados em até 3s
- `[NOVO]` Exibir total de resultados encontrados
- `[NOVO]` Histórico das últimas 10 buscas por usuário
- `[CORREÇÃO-ARQ]` A busca deve ser processada no backend e retornar dados já tratados ao frontend via JSON — o frontend não deve filtrar dados recebidos da API externa

---

### US09 — Filtros avançados

**Como** usuário, **quero** filtrar por parlamentar, partido, data e subtema, **para que** eu refine minha busca com precisão.

**Critérios de aceitação:**

- Filtros por parlamentar, partido, data e subtema
- Filtros combináveis entre si (lógica AND)
- Atualização dinâmica dos resultados sem recarregar a página
- `[NOVO]` Filtros aplicados devem ser exibidos como tags removíveis individualmente
- `[NOVO]` Deve haver opção de limpar todos os filtros com um único clique
- `[NOVO]` Estado dos filtros deve ser preservado ao navegar entre páginas
- `[NOVO]` Deve ser possível salvar combinações de filtros como favoritos (opcional)

---

### US10 — Paginação dos resultados

**Como** usuário, **quero** ver resultados paginados, **para que** a navegação seja organizada.

**Critérios de aceitação:**

- Limite de itens por página configurável (10, 25 ou 50)
- Navegação entre páginas com anterior/próximo e acesso direto por número
- `[NOVO]` Exibir intervalo de itens visíveis (ex: "21–40 de 312 resultados")
- `[NOVO]` URL deve refletir a página atual para permitir compartilhamento de link

---

## Épico 4 — Indicadores e Análises

### US11 — Visualização de indicadores

**Como** analista, **quero** ver gráficos sobre as proposições, **para que** eu identifique padrões e tendências.

**Critérios de aceitação:**

- Gráfico de volume de proposições por subtema
- Evolução temporal de proposições ao longo do tempo
- Ranking dos parlamentares mais ativos
- `[NOVO]` Gráficos devem ser interativos (hover com detalhes, zoom)
- `[NOVO]` Deve ser possível filtrar o período analisado diretamente no gráfico
- `[NOVO]` Indicadores devem atualizar automaticamente com novos dados coletados
- `[CORREÇÃO-ARQ]` Os dados para os gráficos devem ser entregues pelo backend já agregados (ex: `{"ano": 2024, "total": 1523}`) — o frontend não deve calcular agregações sobre listas brutas

---

### US12 — Identificação de novos temas emergentes

**Como** analista, **quero** identificar novos temas emergentes, **para que** eu acompanhe tendências legislativas.

**Critérios de aceitação:**

- Detecção automática de termos com crescimento acelerado de frequência
- Destaque visual de novos termos na interface
- `[NOVO]` Comparar frequência do tema atual versus mesmo período do ano anterior
- `[NOVO]` Gerar alerta automático quando tema emergente ultrapassar threshold configurável
- `[NOVO]` Exibir linha do tempo do crescimento do tema

---

### US13 — Estatísticas automáticas resumidas

**Como** usuário, **quero** ver estatísticas resumidas, **para que** eu entenda rapidamente o panorama dos dados.

**Critérios de aceitação:**

- `[NOVO]` Exibir total de proposições coletadas no período selecionado
- `[NOVO]` Mostrar distribuição percentual por subtema
- `[NOVO]` Exibir variação em relação ao período anterior (ex: +12%)
- `[NOVO]` Estatísticas devem ser recalculadas automaticamente a cada atualização
- `[NOVO]` Deve exibir data e hora da última atualização dos dados
- `[NOVO]` A interface deve exibir aviso informando que os dados são baseados em tramitações e podem não refletir alterações editoriais sem movimentação processual

---

## Épico 5 — Visualização de Dados

### US14 — Dashboard interativo

**Como** usuário, **quero** acessar dashboards interativos, **para que** eu explore os dados facilmente.

**Critérios de aceitação:**

- Gráficos interativos com clique, hover e filtro direto no gráfico
- Atualização dinâmica sem recarregamento de página
- `[NOVO]` Widgets do dashboard devem ser reorganizáveis pelo usuário
- `[NOVO]` Dashboard deve ter versão para impressão e exportação em PDF
- `[NOVO]` Deve suportar pelo menos 5 widgets simultâneos sem perda de performance
- `[CORREÇÃO-ARQ]` Todos os dados exibidos no dashboard devem ser consumidos do backend via Fetch API — nenhum dado deve vir de chamadas diretas à API da Câmara pelo frontend

---

## Épico 6 — Detalhamento das Proposições

### US15 — Visualizar detalhes de uma proposição

**Como** usuário, **quero** ver os detalhes completos de uma proposição, **para que** eu entenda seu conteúdo e situação.

**Critérios de aceitação:**

- Exibir: título, autor, partido, data de apresentação e situação atual
- Link direto para o documento oficial na fonte legislativa
- `[NOVO]` Exibir ementa completa da proposição
- `[NOVO]` Exibir histórico de tramitação em linha do tempo
- `[NOVO]` Exibir subtemas classificados com respectivo score de confiança
- `[NOVO]` Exibir proposições relacionadas sugeridas pelo sistema
- `[NOVO]` Botão de compartilhamento da proposição via link direto

---

## Épico 7 — Alertas e Monitoramento

### US16 — Histórico de mudanças em proposições

**Como** administrador, **quero** visualizar mudanças ocorridas nas proposições, **para que** eu acompanhe alterações e garanta rastreabilidade.

**Critérios de aceitação:**

- `[NOVO]` Exibir diff entre versões (campo alterado, valor anterior e novo valor)
- `[NOVO]` Registrar usuário ou sistema responsável por cada mudança
- `[NOVO]` Histórico deve ser auditável e não editável
- `[NOVO]` Filtrar histórico por período, tipo de mudança ou responsável

---

## Épico 9 — Usabilidade e Performance

### US17 — Interface responsiva

**Como** usuário, **quero** acessar o sistema em qualquer dispositivo, **para que** eu tenha uma boa experiência independentemente da tela.

**Critérios de aceitação:**

- Layout funcional em mobile (320px), tablet e desktop
- `[NOVO]` Componentes adaptados para interação por toque em dispositivos móveis
- `[NOVO]` Imagens e assets otimizados por breakpoint
- `[NOVO]` Acessibilidade: contraste WCAG AA, navegação por teclado e suporte a leitores de tela

---

### US18 — Performance do sistema

**Como** usuário, **quero** respostas rápidas do sistema, **para que** o uso seja eficiente.

**Critérios de aceitação:**

- Tempo de resposta máximo de 3s para 95% das requisições
- `[NOVO]` Sistema deve suportar pelo menos 200 usuários simultâneos sem degradação
- `[NOVO]` Lazy loading aplicado em listas longas e dashboards
- `[NOVO]` Monitoramento de performance com alertas automáticos de violação de SLA
- `[NOVO]` Tempo de primeiro carregamento (LCP) abaixo de 2,5s
- `[CORREÇÃO-ARQ]` A performance é garantida pelo modelo de dados pré-processados: o backend entrega dados prontos ao frontend, eliminando processamento em tempo real no lado do cliente

---

## Épico 10 — Autenticação e Conta

O sistema adota Google OAuth 2.0 como único método de autenticação. O login serve para personalização (favoritos, histórico, notificações) — não há dados sensíveis envolvidos.

Fluxo: Frontend → Login Google → Backend recebe token → valida → busca ou cria usuário → cria sessão → usuário autenticado.

---

### US19 — Login com conta Google

**Como** usuário, **quero** fazer login com minha conta Google, **para que** eu acesse funcionalidades personalizadas de forma simples e rápida.

**Critérios de aceitação:**

- `[CORREÇÃO-LOGIN]` Fluxo de autenticação via Google OAuth 2.0 implementado no módulo `backend/auth/`
- `[CORREÇÃO-LOGIN]` O sistema não deve armazenar senha — apenas o token de acesso e o identificador Google do usuário
- `[CORREÇÃO-LOGIN]` O token de acesso deve ser armazenado em httpOnly cookie para evitar exposição via JavaScript
- `[NOVO]` Exibir mensagem de erro amigável caso o login falhe ou seja cancelado pelo usuário
- `[NOVO]` Botão de login deve estar visível e acessível na página inicial sem navegação adicional
- `[NOVO]` O sistema deve solicitar apenas os escopos mínimos necessários ao Google (email e nome de perfil)
- `[CORREÇÃO-ARQ]` No primeiro login, o backend deve criar automaticamente um registro na tabela `users` com e-mail, nome e foto do perfil Google, atribuindo perfil padrão `cidadão`; em logins subsequentes, atualizar os dados se tiverem mudado

---

### US20 — Redirecionamento seguro pós-login

**Como** usuário, **quero** ser redirecionado de forma segura de volta ao sistema após o login com Google, **para que** minha sessão seja corretamente iniciada e eu continue de onde estava.

**Critérios de aceitação:**

- `[NOVO]` Redirecionar para a URL original solicitada antes do login
- `[NOVO]` Token de sessão deve ter validade máxima de 24h
- `[NOVO]` Proteção contra CSRF e open redirect implementada
- `[CORREÇÃO-LOGIN]` A callback URL registrada no Google Cloud Console deve ser validada no backend antes de processar o retorno

---

### US21 — Persistência de sessão após login

**Como** usuário autenticado, **quero** permanecer logado mesmo após fechar o aplicativo, **para que** eu não precise fazer login com frequência.

**Critérios de aceitação:**

- `[NOVO]` Sessão persistida via refresh token com rotação automática
- `[NOVO]` Opção "lembrar por 30 dias" com consentimento explícito do usuário
- `[NOVO]` Invalidação da sessão ao clicar em "sair"
- `[CORREÇÃO-LOGIN]` Revogação do token Google deve ser acionada no logout para encerrar a sessão também no provedor

---

### US-HIST — Registro estruturado do histórico de interações `[NOVA US]`

**Como** sistema, **quero** registrar em banco de dados relacional as interações dos usuários com as proposições, **para que** seja possível exibir histórico de navegação e auditar o uso da plataforma.

Utiliza a tabela `historico` com campos `user_id`, `proposicao_id`, `tipo_acao` (visualizacao, busca, favorito) e `timestamp`. O registro é feito exclusivamente pelo backend.

**Critérios de aceitação:**

- `[NOVO]` Toda visualização de detalhe de proposição deve gerar um registro na tabela `historico`
- `[NOVO]` Toda busca realizada deve ser registrada com o termo buscado e os filtros aplicados
- `[NOVO]` O usuário deve conseguir visualizar seu próprio histórico (últimas 30 interações)
- `[NOVO]` O usuário deve poder limpar seu histórico a qualquer momento
- `[NOVO]` Administradores devem conseguir consultar o histórico agregado (acessos por proposição e por período)
- `[NOVO]` Dados de histórico não devem ser compartilhados entre usuários
- `[NOVO]` O registro de histórico deve ser assíncrono e não deve impactar o tempo de resposta da interface
- `[NOVO]` Em conformidade com a LGPD, o usuário deve ser informado sobre o que é registrado e ter opção de desativar o rastreamento
- `[CORREÇÃO-ARQ]` O registro na tabela `historico` deve ser feito exclusivamente pelo backend — o frontend apenas envia o evento via Fetch API