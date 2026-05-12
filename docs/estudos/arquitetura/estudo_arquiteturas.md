# Estudo: Arquitetura de Software

Este documento reúne os estudos sobre arquitetura de software, cobrindo conceitos fundamentais, padrões arquiteturais, princípios de design e exemplos reais, com aplicação ao projeto da disciplina.

---

## O que é Arquitetura de Software

Arquitetura de software é a estrutura fundamental de um sistema, que define seus componentes, suas relações e seus princípios de projeto e evolução.

Ela não trata apenas da estrutura, mas também das **decisões técnicas mais importantes** que impactam diretamente atributos de qualidade como desempenho, segurança, escalabilidade e manutenibilidade. Essas decisões costumam ser difíceis de mudar depois que o sistema está em produção, o que torna a arquitetura uma etapa crítica do desenvolvimento.

Um padrão arquitetural é uma solução já estabelecida para problemas conhecidos no desenvolvimento de software, testada em projetos reais e amplamente aceita no mercado. Suas vantagens incluem:

- maior flexibilidade e escalabilidade
- facilidade de manutenção e evolução
- segurança
- melhor desempenho
- redução de custos e riscos

Uma boa arquitetura não é apenas a que resolve o problema atual, mas a que permite que o sistema continue saudável e sustentável no futuro.

---

## Arquitetura vs. Design de Software

### Arquitetura de Software

É sobre **como o sistema é organizado como um todo** — visão macro, alto nível.

Envolve decisões de alto impacto, como:

- escolha entre padrões de arquitetura
- tipo de comunicação (REST, mensageria, eventos)
- uso de banco de dados (relacional ou NoSQL)
- estratégias de escalabilidade e disponibilidade

Essas são chamadas de **decisões arquiteturalmente significativas**, pois são difíceis de reverter depois.

### Design de Software

É sobre **como cada parte interna é construída** — visão micro, baixo nível.

Envolve:

- estrutura de classes e objetos
- escolha de padrões de projeto (Design Patterns)
- organização de métodos e responsabilidades
- legibilidade e manutenibilidade do código

### Relação entre os dois

Arquitetura e design não são coisas separadas, mas **níveis diferentes da mesma decisão**:

- a arquitetura define limites e regras
- o design preenche esses limites com implementação

A arquitetura guia o design, e o design concretiza a arquitetura.

### Erros comuns

Um erro frequente é confundir os dois níveis:

- "Escolher microsserviços" é uma decisão de **arquitetura**
- "Usar padrão Factory" é uma decisão de **design**

Outro erro é tentar resolver problemas arquiteturais com design: problemas de escalabilidade não se resolvem apenas com código melhor.

---

## Padrões arquiteturais

### Arquitetura monolítica

Um sistema monolítico é uma aplicação onde tudo fica em um único bloco: interface, regras de negócio e banco de dados, rodando no mesmo processo.

#### Como funciona

- todas as partes são dependentes entre si
- mudanças em uma parte podem afetar o sistema inteiro
- geralmente é gerado um único pacote para rodar

#### Tipos de monolito

Segundo Sam Newman, existem três tipos:

- **monolito simples** — tudo junto em um único processo
- **monolito modular** — dividido em módulos, mas ainda é um sistema único
- **monolito distribuído** — partes separadas, mas muito dependentes (pode virar bagunça)

#### Vantagens

- simples de desenvolver
- rápido para começar (ótimo para projetos pequenos)
- fácil de fazer deploy

#### Desvantagens

- difícil de escalar
- mudanças podem quebrar outras partes
- um erro pode derrubar tudo (ponto único de falha)

---

### Arquitetura baseada em microsserviços

O sistema é dividido em vários serviços pequenos e independentes, cada um responsável por uma funcionalidade específica.

#### Como funciona

- cada serviço é independente
- cada um pode ter seu próprio banco de dados
- os serviços se comunicam por APIs ou mensageria
- é possível usar linguagens e tecnologias diferentes por serviço

#### Vantagens

- mais flexível
- mais fácil de escalar (só o que precisa)
- times podem trabalhar independentemente
- facilita adicionar novas funcionalidades

#### Desvantagens

- mais complexo de implementar
- maior custo de infraestrutura
- comunicação entre serviços pode gerar problemas
- mais difícil de manter e monitorar

#### Conclusão

Ótimo para sistemas grandes e em crescimento, mas só vale a pena se a complexidade for justificada.

---

### Arquitetura MVC (Model-View-Controller)

Padrão muito comum no desenvolvimento web, usado para organizar o código e separar responsabilidades em três partes principais.

#### Como funciona

- **Model (Modelo)** — contém as regras de negócio e acessa os dados (banco, APIs)
- **View (Visão)** — responsável pela interface com o usuário
- **Controller (Controlador)** — faz a ligação entre Model e View, recebe ações do usuário e decide o que fazer

#### Fluxo básico

1. Usuário interage com a View
2. A View envia a ação para o Controller
3. O Controller chama o Model
4. O Model processa os dados
5. O resultado volta para a View
6. A View mostra para o usuário

#### Vantagens

- código mais organizado
- facilita manutenção
- permite reuso de código
- mais fácil trabalhar em equipe

#### Desvantagens

- pode ser mais complexo no início
- exige boa organização para não virar bagunça

---

### Arquitetura em camadas (Layers)

Organiza o sistema em níveis, onde cada camada tem uma função específica e depende da camada abaixo.

#### Como funciona

- o sistema é dividido em camadas
- cada camada usa os serviços da camada inferior
- a comunicação geralmente segue um fluxo de cima para baixo

#### Exemplo de camadas

- **Interface (UI)** — tela que o usuário vê (frontend)
- **Camada de aplicação** — controle de fluxo, autenticação, regras básicas
- **Lógica de negócio** — regras principais do sistema
- **Infraestrutura** — banco de dados, sistema operacional

#### Diferença em relação ao MVC

- MVC separa por tipo de responsabilidade (Model, View, Controller)
- Camadas separa por níveis do sistema

São conceitos diferentes, mas podem ser usados juntos.

#### Vantagens

- organização clara do sistema
- facilita divisão entre equipes
- boa para sistemas grandes e estruturados

#### Desvantagens

- pode adicionar complexidade
- pode gerar dependência rígida entre camadas
- às vezes pode impactar performance

#### Quando usar

- quando há times diferentes trabalhando
- quando o sistema precisa de segurança por níveis
- quando se quer evoluir um sistema existente

---

## Princípios fundamentais

### Baixo acoplamento (Low Coupling)

As partes do sistema têm pouca dependência entre si. Mudanças em uma parte não quebram o resto.

- quanto menos dependência, melhor
- facilita mudanças e manutenção
- facilita testes

Evite depender diretamente — use abstrações.

---

### Alta coesão (High Cohesion)

Cada classe ou módulo tem uma responsabilidade bem definida. Tudo dentro dela está relacionado.

- uma classe, uma responsabilidade
- código mais legível e fácil de manter
- facilita reaproveitamento

---

### Separação de responsabilidades (Separation of Concerns)

Dividir o sistema em partes onde cada uma cuida de um aspecto específico. Evita misturar coisas diferentes.

- View — interface
- Service — regras
- Repository — banco

---

### Relação entre os princípios

- **Separação de responsabilidades** — divide o sistema em áreas de funcionamento
- **Alta coesão** — cada parte faz bem seu papel
- **Baixo acoplamento** — as partes não ficam dependentes demais

---

## Exemplos reais

### Netflix

Arquitetura de microsserviços, altamente distribuída, rodando na nuvem (AWS). Cada funcionalidade é um serviço independente (catálogo, recomendações, streaming, autenticação), comunicando-se via APIs.

- precisava escalar para milhões de usuários com disponibilidade 24/7
- trade-off: muito complexo e alto custo de infraestrutura

---

### Amazon

Pioneira em microsserviços, com arquitetura em camadas internamente. A regra interna exige que times se comuniquem apenas por APIs, garantindo baixo acoplamento e escalabilidade extrema.

- trade-off: complexidade organizacional e técnica

---

### Instagram

Começou como monolito (Django) e depois evoluiu com partes distribuídas. A decisão de começar simples e escalar depois mostrou que não é necessário começar com microsserviços.

- trade-off: escalar monolito exige engenharia avançada

---

### WhatsApp

Sistema distribuído baseado em Erlang, focado em mensageria. Servidores lidam com milhões de conexões simultâneas em tempo real.

- decisão: escolher tecnologia que suporta concorrência massiva
- trade-off: menos flexível para features complexas

---

### Conclusão dos exemplos

Não existe "melhor arquitetura" universal. Tudo depende de escala, complexidade, equipe e objetivo do negócio:

- sistemas pequenos → monolito com simplicidade
- sistemas grandes → microsserviços ou distribuído

---

## Aplicação no projeto

### Projeto: Monitoramento Legislativo — Proteção de Crianças na Internet

Plataforma para monitorar, classificar e analisar proposições legislativas sobre proteção de crianças e adolescentes no ambiente digital, com foco em cyberbullying, exploração sexual online, proteção de dados de menores, regulação de plataformas digitais e exposição a conteúdo nocivo.

### Arquitetura ideal

**Monolito em camadas + MVC**

Justificativa:

- complexidade média, compatível com projeto acadêmico
- mais simples de desenvolver e manter
- permite evolução futura

### Estrutura

- **Frontend (View)** — dashboards, gráficos, filtros
- **Backend (Controller / API)** — recebe requisições de busca, filtros e relatórios
- **Service (Lógica de negócio)** — classificação por tema, análise de dados, processamento com NLP
- **Repository (Dados)** — acesso ao banco e integração com APIs legislativas
- **Infraestrutura** — banco de dados e APIs externas

---

## Resumo

### Arquitetura vs. Design

- arquitetura → visão macro, organização do sistema, escolha de tecnologias e padrões
- design → visão micro, classes, métodos, implementação

### Padrões arquiteturais

- **Monolito** — tudo em um sistema único, simples no início, difícil de escalar
- **Microsserviços** — serviços independentes, alta escalabilidade, alta complexidade
- **MVC** — divide em Model, View e Controller, foca na organização do código
- **Camadas** — divide o sistema por níveis (UI → aplicação → negócio → dados)

### Princípios

- separação de responsabilidades → divide o sistema em áreas
- alta coesão → cada parte faz uma coisa bem definida
- baixo acoplamento → partes não dependem demais entre si

### Regra geral

- sistemas pequenos → monolito com simplicidade
- sistemas grandes → microsserviços