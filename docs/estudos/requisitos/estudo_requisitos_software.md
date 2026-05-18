# Estudo: Requisitos de Software

Link de referência: https://engsoftmoderna.info/cap3.html

---

## 1. Conceito de requisito

Requisitos de software são descrições do comportamento do sistema, indicando o que ele deve fazer, os serviços que oferece e as restrições sobre seu funcionamento, refletindo as necessidades do cliente.

### Tipos de requisitos

**Requisitos funcionais** — o que o cliente pede que o software faça. Exemplo: "o sistema deve emitir relatórios de vendas".

**Requisitos não-funcionais** — propriedades de qualidade e restrições, como desempenho, segurança, usabilidade, disponibilidade e portabilidade.

**Requisitos de domínio** — surgem das regras, leis e padrões da área de aplicação. Exemplo: "a média final deve ser calculada conforme o regulamento institucional".

**Requisitos de usuário** — alto nível, escritos em linguagem natural, descrevendo o que o sistema deve fornecer. Estão mais próximos do problema.

**Requisitos de sistema** — definem exatamente o que o software deve fazer (especificações de requisito). Estão mais próximos da solução.

### Stakeholders

Um stakeholder é um indivíduo ou grupo que tem interesse em uma empresa, podendo impactar ou ser impactado pelo negócio. Identificar os stakeholders é importante porque são eles que legitimam as iniciativas e influenciam os resultados.

### Engenharia de Requisitos

É a base da Engenharia de Software e alimenta todas as fases subsequentes — design, codificação, testes e manutenção. Erros nessa etapa respondem por 50% a 80% dos defeitos em projetos. Negligenciar requisitos garante atrasos, estouro de orçamento e entregas que não atendem às necessidades reais.

### Ciclo de vida dos requisitos

Segundo a NBR ISO/IEC 12207:1998, o ciclo de vida é a estrutura contendo processos, atividades e tarefas envolvidas no desenvolvimento, operação e manutenção de um produto de software, abrangendo desde a definição dos requisitos até o término de seu uso.

| Modelo | Principais características | Vantagens | Problemas/Riscos | Indicado para |
| --- | --- | --- | --- | --- |
| Cascata | Sequencial e linear, fases bem definidas, forte documentação | Simples, fácil estimar custo e prazo | Rígido, cliente só vê o produto no final | Projetos com requisitos estáveis |
| Modelo em V | Evolução do cascata, cada fase tem fase correspondente de teste | Maior garantia de qualidade | Ainda é rígido, mudanças geram alto custo | Sistemas críticos (embarcados, regulados) |
| Incremental | Sistema construído em partes, cada entrega adiciona funcionalidades | Entrega valor cedo, mais flexível | Requer boa arquitetura, risco de integração | Projetos divisíveis em módulos |
| Evolutivo | Versões sucessivas refinadas com feedback do cliente | Reduz risco de má interpretação | Escopo pode crescer demais | Requisitos pouco definidos |
| RAD | Desenvolvimento rápido, atividades paralelas | Alta velocidade de entrega | Pode perder qualidade | Projetos pequenos/médios com prazo curto |
| Prototipagem | Criação de protótipos para entender requisitos | Esclarece requisitos confusos | Protótipo pode virar produto mal estruturado | Sistemas inovadores ou pouco claros |
| Espiral | Iterativo e guiado por riscos | Excelente para projetos complexos | Alto custo, difícil prever prazo | Grandes sistemas com alto risco |
| RUP | Iterativo e incremental, 4 fases, orientado a casos de uso | Processo organizado, controle de riscos | Pode ser burocrático | Projetos médios/grandes em empresas estruturadas |

---

## 2. Processo de Engenharia de Requisitos

### Elicitação de requisitos

Atividades relacionadas à descoberta e entendimento dos requisitos, por meio de interações dos desenvolvedores com os stakeholders. Técnicas utilizadas:

- entrevistas com stakeholders
- aplicação de questionários
- leitura de documentos da organização
- workshops com usuários
- implementação de protótipos
- análise de cenários de uso

Para produtos inovadores, é impossível descobrir todos os requisitos no início do desenvolvimento. Por isso, a construção dos requisitos precisa ser colaborativa, envolvendo Product Manager (PM), Product Owner (PO) e o time de desenvolvimento.

### Validação

Envolve a confirmação de que as especificações documentadas estão corretas, completas e compreendidas por todos os envolvidos. Técnicas:

- **Revisões** — análise dos requisitos por stakeholders e especialistas (ex: Tech Leads)
- **Prototipagem** — modelos simplificados do sistema para coleta de feedback (ferramentas: Figma, Adobe XD)
- **Simulações** — representações virtuais do sistema para prever comportamento em diferentes cenários

### Gerenciamento de requisitos

Inclui o controle das mudanças, onde qualquer alteração é registrada, avaliada e aprovada antes de ser adotada. Ferramentas comuns: Jira, IBM DOORS, Trello.

---

## 3. Documentação

### Documento de Visão

Documento de alto nível que descreve o propósito, objetivos, stakeholders e funcionalidades principais do produto.

| Item | Descrição |
| --- | --- |
| Problema | O problema que o sistema resolve |
| Objetivos | O que se espera alcançar |
| Stakeholders | Quem são os envolvidos |
| Usuários-alvo | Perfis de usuário |
| Visão geral do produto | Descrição sucinta do que será entregue |
| Principais funcionalidades | Lista de alto nível |
| Restrições | Orçamento, prazo, tecnologia, regulatórias |

### SRS (Software Requirements Specification)

Plano ou roteiro para o software que será construído. Elementos:

- **Propósito** — por que o software está sendo desenvolvido
- **Descrição** — o que o software fará
- **Requisitos** — funcionalidades específicas e restrições
- **Links** — conexão entre histórias de usuário e requisitos
- **Processo de aprovação** — alinhamento entre as partes interessadas

Participação por papel: Product Owners e analistas de negócio definem requisitos; desenvolvedores entendem o que construir; testadores criam casos de teste; gerentes acompanham escopo; clientes e stakeholders aprovam.

### Padrão IEEE 830 / ISO/IEC/IEEE 29148

Após a especificação, os requisitos devem ser verificados e validados. Segundo o IEEE 830, precisam ser:

- **Corretos** — refletir exatamente o que o sistema deve fazer
- **Precisos** — não permitir múltiplas interpretações
- **Completos** — conter todas as informações necessárias
- **Consistentes** — sem conflitos entre si
- **Verificáveis** — testáveis, permitindo comprovar seu atendimento

A ISO/IEC/IEEE 29148 define processos, produtos e diretrizes para a engenharia de requisitos ao longo de todo o ciclo de vida, abordando requisitos de negócio, de partes interessadas e de sistema.

### Backlog do Produto

Lista ordenada de todos os requisitos e funcionalidades do produto, gerenciada exclusivamente pelo Product Owner. Os itens no topo são mais detalhados e prontos para desenvolvimento; os itens da base são mais amplos. O Backlog é dinâmico e evolui conforme o produto e o mercado.

---

## 4. Modelagem de Requisitos

### Casos de Uso

Descrevem funções que o sistema desempenha para alcançar a meta do usuário, produzindo um resultado observável e valioso. Contêm informações sobre o sistema, os usuários, os relacionamentos entre eles e o comportamento requerido — sem descrever como o sistema é executado internamente.

Usos: determinar requisitos, descrever o que o sistema deve fazer, fornecer base para testes.

O Diagrama de Caso de Uso é um índice gráfico que representa atores (bonecos) e casos de uso (elipses), com dois tipos de relacionamento: ator–caso de uso (participação) e caso de uso–caso de uso (inclusão ou extensão).

### UML

Linguagem de Modelagem Unificada utilizada para visualizar sistemas e software. Engenheiros criam diagramas UML para entender designs, arquitetura de código e implementação proposta de sistemas complexos. Simplifica informações em uma referência visual mais fácil de entender, usando um método padronizado para capturar ideias conceituais.

### BPMN

BPMN (Business Process Model and Notation) é uma notação gráfica padronizada para modelar e documentar processos de negócio. Elementos principais:

- **Eventos** — círculos que representam algo que acontece
- **Atividades** — processos de negócio executados (ex: "gerar um relatório")
- **Portas de entrada** — diamantes que direcionam fluxos alternativos
- **Fluxo de sequência** — linha sólida com seta indicando a ordem das atividades
- **Fluxo de mensagens** — linha tracejada representando comunicação entre organizações
- **Raias/piscina** — retângulos que organizam aspectos do processo em fluxograma multifuncional
- **Artefatos** — objetos de dados, grupos e anotações de texto

### User Stories

Histórias de Usuário são documentos usados em metodologias ágeis para descrever funcionalidades de uma solução. Seu principal objetivo é **comunicar** — transmitir claramente a visão do cliente e orientar o time de desenvolvimento.

Uma User Story deve conter dois elementos principais:

**Descrição** — segue o modelo "quem – o quê – por quê" (role–feature–benefit):

> "Como analista de crédito, quero visualizar as informações de risco do cliente, para ter assertividade na aprovação de crédito."

A estrutura sugerida é: contextualização + (quem, o quê, por quê) + protótipos.

**Critérios de Aceitação** — condições que precisam ser atendidas para a funcionalidade ser considerada pronta. Baseiam-se em regras de negócio, UX, segurança e outros aspectos relevantes. Um formato comum é o modelo Given/When/Then (Dado/Quando/Então), herdado do BDD.

---

## 5. Validação e Verificação

**Verificação** — garante que o software foi desenvolvido corretamente, em conformidade com as especificações. Envolve revisões de código, inspeções de documentos e testes unitários. Pergunta central: *"Estamos construindo o produto certo?"*

**Validação** — garante que o produto final atende às expectativas do cliente. Envolve testes funcionais, testes de aceitação e simulações. Pergunta central: *"Estamos construindo o produto certo para o usuário?"*

### Revisões

Buscam encontrar erros, anomalias e omissões em qualquer estágio do desenvolvimento, podendo analisar e verificar qualquer produto do processo.

### Prototipação

Criação de versões iniciais e simplificadas do sistema antes da implementação, permitindo que o cliente visualize e interaja com as principais funcionalidades nas fases iniciais do projeto.

### Teste Baseado em Requisitos (RBT)

Valida o software contra especificações funcionais, garantindo que cada requisito seja testado. A **Matriz de Rastreabilidade de Requisitos (RTM)** vincula requisitos a casos de teste, facilitando cobertura total, detecção precoce de erros e gestão de mudanças.

Vantagens: aumenta a confiança na qualidade, reduz custos ao detectar defeitos no início e facilita auditorias e conformidade.

---

## 6. Gerenciamento de Requisitos

### Gerenciamento de mudanças

Alterações nas especificações são naturais ao longo do projeto. Para controlá-las, utiliza-se a matriz de rastreabilidade e um processo formal de avaliação e aprovação.

Toda solicitação de mudança deve ser documentada com:

- descrição da mudança
- tipo (corretiva, preventiva, reparo de defeito etc.)
- justificativa
- impactos e benefícios esperados
- alternativas caso não seja implementada

Todas as solicitações — aprovadas ou não — devem ser registradas e comunicadas às partes interessadas.

### Versionamento

O controle de versão (VCS) rastreia todas as alterações feitas no código-fonte, permitindo consultar históricos, comparar versões e reverter mudanças. Cria uma fonte única de verdade, facilitando colaboração e revisão de código.

**Tipos de sistemas:**

- **Centralizado (CVCS)** — repositório único central
- **Distribuído (DVCS)** — cada desenvolvedor possui cópia completa do repositório
- **Baseado em bloqueio** — arquivos bloqueados para evitar edições simultâneas
- **Otimista** — permite edições simultâneas e resolve conflitos na integração

**Principais sistemas:** Git (distribuído, open source, mais popular), SVN (centralizado, simples), Mercurial (distribuído, interface intuitiva).

### Matriz de Rastreabilidade de Requisitos (RTM)

Documento que liga cada requisito a artefatos relacionados — especificações de design, tarefas de desenvolvimento, casos de teste e entregas. Garante que nenhum requisito seja negligenciado e facilita a análise de impacto de mudanças.

**Tipos de rastreabilidade:**

- **Futura** — liga requisitos aos elementos de design e testes
- **Reversa** — liga elementos de projeto de volta aos requisitos originais
- **Bidirecional** — combina as duas para máximo controle e cobertura

---

## MVP

O MVP (Produto Mínimo Viável) defende a eliminação de desperdícios. Consiste em desenvolver uma versão simples do produto com requisitos mínimos suficientes para testar uma hipótese de negócio, em vez de longos levantamentos ou pesquisas de mercado pouco confiáveis.

O método Lean Startup segue o ciclo: **Construir → Medir → Aprender**

A partir do aprendizado, três caminhos são possíveis:

1. ajustar e repetir o ciclo, refinando o MVP
2. escalar o produto, caso haja adequação ao mercado (market fit)
3. desistir ou pivotar, criando um novo MVP com base no aprendizado

O foco deve estar em **métricas acionáveis** (taxa de conversão, custo de aquisição, valor médio de compra), evitando **métricas de vaidade** como número de visualizações.

Para produtos digitais, utilizam-se métricas de funil: aquisição (visitantes), ativação (cadastros), retenção (retorno), receita (compras) e recomendação (indicações).

---

## Vídeos recomendados

- https://youtu.be/YLd6AWKVyas?si=00U5Eq-sF_Hz5C5_
- https://youtu.be/ptreLvwOXyw?si=DsCG2BoFbvkvgI9v