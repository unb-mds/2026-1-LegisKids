# Requisitos de Software (Anotação)

# 1. Conceito de requisito

Requisitos de Software são descrições do comportamento do software, indicando o que o sistema/software deve fazer, serviços que ele oferece e restrições sobre o seu funcionamento. Refletindo a necessidade do cliente em um determinado pedido.

#### São divididos em:

- **Requisitos Funcionais:** É aquilo que o cliente pede para que o software faça, como "o sistema deve emitir relatórios de vendas" ou "o usuário deve conseguir redefinir sua senha".
- **Requisitos Não-Funcionais:** Definem propriedades de qualidade e restrições, como desempenho (tempo de resposta), segurança (criptografia), usabilidade (intuitividade), disponibilidade e portabilidade.
- **Requisito de domínio:** É aquele que surge das regras, leis, padrões e características específicas da área de aplicação do sistema. Conectando o sistema ao mundo real, como por exemplo: A média final deve ser calculada conforme o regulamento institucional (ex: média ≥ 6 para aprovação).

Alguns estudos também classificam alguns requisitos como:

- **Requisitos de Usuário**: Alto nível, escrito em língua natural, explicando quais serviços o sistema deve fornecer ao usuário e o que o sistema não pode fazer.
- **Requisitos de Sistema**: Deve definir exatamente o que o software deve fazer, podendo ser chamado também de “especificações de requisito”.

Portanto, requisitos de usuário estão mais próximos do problema, enquanto que requisitos de sistema estão mais próximos da solução.

Links sobre Requisitos Funcionais/Não-Funcionais: 

https://youtu.be/YLd6AWKVyas?si=00U5Eq-sF_Hz5C5_

https://youtu.be/ptreLvwOXyw?si=DsCG2BoFbvkvgI9v

## **O que é um stakeholder?**

Um **stakeholder** é um indivíduo ou grupo que tem interesse em uma empresa, podendo impactar ou ser impactado pelo negócio. Investidores, clientes, funcionários e fornecedores. Entender quais são os seus **stakeholders** é importante porque são eles que legitimam as iniciativas de um negócio, influenciando seus resultados.

#### Engenharia de Requisitos:

A Engenharia de Requisitos é a base da Engenharia de Software. Ela alimenta todas as fases subsequentes – design, codificação, testes e manutenção. Erros nessa etapa são os mais caros e frequentes, respondendo por 50% a 80% dos defeitos em projetos. Negligenciar requisitos é garantir atrasos, estouro de orçamento e entregas que não atendem às necessidades reais.

#### Ciclo de vida dos requisitos

De acordo com a NBR ISO/IEC 12207:1998, o ciclo de vida é a “**Estrutura contendo processos, atividades e tarefas envolvidas no desenvolvimento, operação e manutenção de um produto de software, abrangendo a vida do sistema, desde a definição de seus requisitos até o término de seu uso.**”

| Modelo | Principais Características | Vantagens | Problemas / Riscos | Indicado Para |
| --- | --- | --- | --- | --- |
| **Cascata** | Sequencial e linear; fases bem definidas; forte documentação; planejamento inicial detalhado | Simples; fácil estimar custo e prazo | Rígido; cliente só vê o produto no final; difícil lidar com mudanças | Projetos com requisitos estáveis |
| **Modelo em V** | Evolução do cascata; cada fase de desenvolvimento tem fase correspondente de teste; foco forte em validação | Maior garantia de qualidade; testes planejados desde o início | Ainda é rígido; mudanças geram alto custo | Sistemas críticos (ex: embarcados, regulados) |
| **Incremental** | Sistema construído em partes (incrementos); cada entrega adiciona funcionalidades | Entrega valor cedo; maior flexibilidade que cascata | Requer boa arquitetura; risco de integração complexa | Projetos que podem ser divididos em módulos |
| **Evolutivo** | Versões sucessivas refinadas com feedback do cliente; requisitos evoluem | Reduz risco de má interpretação; adaptação constante | Escopo pode crescer demais; exige forte gestão | Requisitos pouco definidos |
| **RAD** | Desenvolvimento rápido; atividades paralelas; uso intenso de ferramentas e reutilização | Alta velocidade de entrega | Pode perder qualidade e desempenho | Projetos pequenos/médios com prazo curto |
| **Prototipagem** | Criação de protótipos para entender requisitos; forte interação com cliente | Esclarece requisitos confusos | Protótipo pode virar produto mal estruturado | Sistemas inovadores ou pouco claros |
| **Espiral** | Iterativo e guiado por riscos; cada ciclo inclui análise de riscos | Excelente para projetos complexos e críticos | Alto custo; difícil previsão de prazo | Grandes sistemas com alto risco |
| **RUP** | Iterativo e incremental; 4 fases (Concepção, Elaboração, Construção, Transição); orientado a casos de uso | Processo organizado; controle de riscos | Pode ser burocrático; exige maturidade | Projetos médios/grandes em empresas estruturadas |

# 2. Processo de Engenharia de Requisitos

## Elicitação de requisitos

São atividades relacionadas com a descoberta e entendimento dos requisitos de um sistema. Sendo interações dos desenvolvedores de um sistema com os seus stakeholders, com o objetivo de descobrir e entender os principais requisitos do sistema que se pretende construir.
Para a realização das elicitações são utilizadas várias técnicas, entre elas:

- Entrevistas com stakeholders
- Aplicação de questionários
- Leitura de documentos e formulários da organização que está contratando o sistema
- Realização de workshops com os usuários
- Implementação de protótipos
- Análise de cenários de uso

Entendemos que, **para produtos inovadores, é impossível descobrir todos os requisitos no início do desenvolvimento**.

Por esse motivo, a construção dos requisitos precisa ser colaborativa. A configuração varia muito, mas podemos ter:

- **Product Manager (PM)** atuando em nível de negócio, definindo visão de produto, métricas e objetivos;
- **Product Owner (PO)**, em contato direto com o time, facilitando o processo de transformar os grandes objetivos em **histórias de usuário**;
- **Time de desenvolvimento**, que participa desse refinamento, executa testes e análises para identificar feedbacks que contribuem para a melhoria contínua do produto; entre outros envolvidos.

## Validação

A validação de requisitos de software envolve a confirmação de que as especificações documentadas estão corretas, completas e compreendidas por todos os envolvidos.

As técnicas que podem ser usadas para essa validação são:

- **Revisões**: envolvem a análise dos requisitos por uma equipe de stakeholders e especialistas, por exemplo, os Tech Leads, garantindo que todos os aspectos sejam confirmados e aceitos;
- **Prototipagem**: consiste em criar modelos simplificados do sistema, que permitem aos usuários interagir e fornecer feedback antes da construção completa do produto. Figma e Adobe XD são ferramentas bastante usadas para isso;
- **Simulações**: utilizam representações virtuais do sistema para prever como ele se comporta em diferentes cenários.

## **Gerenciamento de requisitos**

Fazer um bom gerenciamento de requisitos de software inclui o controle das mudanças, onde **qualquer alteração é registrada, avaliada e aprovada antes de ser adotada**. Para facilitar esse processo, podem ser utilizadas ferramentas de gerenciamento como Jira, IBM DOORS e Trello.

# 3. Documentação

## **Documento de Visão**

**Definição:** Documento de alto nível que descreve o propósito, objetivos, stakeholders e funcionalidades principais do produto, ajudando a visualizar os requisitos e suas interações de forma gráfica, o que facilita o entendimento e a comunicação.

| **Item** | **Descrição** |
| --- | --- |
| Problema | O problema que o sistema resolve |
| Objetivos | O que se espera alcançar |
| Stakeholders | Quem são os envolvidos |
| Usuários-alvo | Perfis de usuário |
| Visão geral do produto | Descrição sucinta do que será entregue |
| Principais funcionalidades | Lista de alto nível |
| Restrições | Orçamento, prazo, tecnologia, regulatórias |

## SRS

Pense em um **SRS (Software Requirements Specification)** como um **plano ou roteiro** para o software que será construído. Os elementos que o compõem incluem:

- **Propósito (Purpose):** Por que o software está sendo desenvolvido.
- **Descrição (Description):** O que o software fará.
- **Requisitos (Requirements):** Funcionalidades específicas e restrições.
- **Links:** Conexão entre histórias de usuário e requisitos específicos.
- **Processo de Aprovação (Approval Process):** Garantia de que todas as partes interessadas estejam alinhadas.

---

Veja como cada papel da equipe participa na produção e uso do SRS:

- **Product Owners e Analistas de Negócio:** Definem os requisitos.
- **Desenvolvedores:** Entendem o que deve ser construído.
- **Testadores:** Criam casos de teste e garantem a validação.
- **Gerentes de Projeto:** Acompanham escopo e progresso.
- **Clientes e Stakeholders:** Aprovam funcionalidades e expectativas.

## Documento de Requisitos — Padrão IEEE 830 - **ISO/IEC/IEEE 29148**

Após a especificação, os requisitos devem ser **verificados e validados** para garantir qualidade. Segundo o padrão IEEE 830, eles precisam ser:

- **Corretos**: refletir exatamente o que o sistema deve fazer.
- **Precisos (não ambíguos)**: não permitir múltiplas interpretações.
- **Completos**: conter todas as informações necessárias.
- **Consistentes**: não apresentar conflitos entre si.
- **Verificáveis**: ser testáveis, permitindo comprovar seu atendimento.

O objetivo é garantir clareza, confiabilidade e possibilidade de teste dos requisitos.

A norma **ISO/IEC/IEEE 29148é um padrão internacional que define os processos, produtos e diretrizes para a engenharia de requisitos em sistemas, softwares e serviços**. Ela estabelece boas práticas para definir, documentar, analisar e gerenciar requisitos ao longo de todo o ciclo de vida, garantindo qualidade, rastreabilidade e consistência.

**Principais aspectos da ISO/IEC/IEEE 29148:**

- **Foco no Requisito:** Define o que constitui um "bom" requisito (ex: claro, consistente, verificável) e como estruturar documentos de requisitos (especificações).
- **Ciclo de Vida:** Aplica-se de forma iterativa e recursiva desde a concepção até a inativação do sistema.
- **Hierarquia de Requisitos:** Aborda requisitos de negócio (necessidades da organização), requisitos de partes interessadas (visão do usuário) e requisitos de sistema (técnicos).
- **Conexão com outras normas:** Oferece diretrizes adicionais para os processos de engenharia de requisitos definidos nas normas **ISO/IEC 12207:2008** e ISO/IEC 15288:2008.
- **Conteúdo dos documentos:** Define o conteúdo normativo para especificações, incluindo o propósito, escopo, regras de negócio e restrições.

## Backlog do Produto

O **Backlog do Produto** é a lista ordenada de todos os requisitos e funcionalidades do produto, gerenciada exclusivamente pelo **Product Owner**. Ele representa a fonte única de mudanças e é refinado continuamente, servindo como principal entrada para cada Sprint.

Os itens no topo são mais detalhados, refinados e prontos para desenvolvimento, enquanto os itens da base são mais amplos e menos detalhados. O Backlog é dinâmico e evolui conforme o produto, o mercado e o entendimento das partes interessadas mudam.

# 4. Modelagem de Requisitos

## Caso de Usos

Um caso de uso descreve uma função que um sistema desempenha para alcançar a meta do usuário. Um caso de uso deve produzir um resultado observável que seja valioso para o usuário do sistema. Os casos de uso contêm informações detalhadas sobre o sistema, os usuários do sistema, os relacionamentos entre o sistema e os usuários e o comportamento requerido do sistema. Os casos de uso não descrevem os detalhes de como o sistema é executado.

É possível utilizar casos de uso para os seguintes objetivos:

- Determinar os requisitos do sistema
- Descrever o que o sistema deve fazer
- Fornecer uma base para teste, para assegurar que o sistema funcione conforme pretendido

Visualmente falando os Diagramas de Caso de Uso é um índice gráfico de casos de uso. Ele representa os atores de um sistema (como pequenos bonecos) e os casos de uso (como elipses). Mostram-se também dois tipos de relacionamento: (1) ligando ator com caso de uso, que indicam que um ator participa de um determinado caso de uso; (2) ligando dois casos de uso, que indicam que um caso de uso inclui ou estende outro caso de uso.

![image.png](image.png)

## UML

O Diagrama UML é uma maneira de visualizar sistemas e software usando a Linguagem de Modelagem Unificada (UML). Engenheiros de software **criam diagramas UML** para entender os designs, a arquitetura do código e a implementação proposta de sistemas de software complexos. Os diagramas UML também são usados para modelar fluxos de trabalho e processos de negócios. A codificação pode ser um processo complicado com muitos elementos inter-relacionados. Muitas vezes, há milhares de linhas de linguagem de programação que podem ser difíceis de entender à primeira vista. Um diagrama UML simplifica essas informações em uma referência visual mais fácil de digerir. Ele usa um método padronizado para escrever um modelo de sistema e capturar ideias conceituais.

Exemplo de Diagrama UML

![image.png](image%201.png)

## BPMN

O **BPMN (Business Process Model and Notation)** é uma notação gráfica padronizada para modelar e documentar processos de negócio, representando visualmente atividades e fluxos de informação.

- **Elementos gráficos encontrados em um BPMN**
    
    **Eventos**: círculos que representam algo que acontece. Dentro do círculo, muitas vezes há ícones que indicam o tipo de evento.
    
    ![image.png](image%202.png)
    
    **Atividades**: processos de negócios que são executados, como “gerar um relatório”.
    
    ![image.png](image%203.png)
    
    **Portas de entrada**: se uma atividade precisa passar por diferentes fluxos de processos de negócios, é necessário desenhar uma porta de entrada em forma de diamante.
    
    ![image.png](image%204.png)
    
    - **Fluxo de sequência**: uma linha e ponta de seta sólida mostrando a ordem em que são realizadas as atividades.
        
        ![Fluxo de Sequência](https://d2slcw3kip6qmk.cloudfront.net/marketing/pages/chart/seo/bpmn/sequence-flow.svg)
        
    - **Fluxo de mensagens**: exibido como uma linha tracejada com um círculo aberto no início da linha e ponta de seta aberta onde termina a linha. Representa quais mensagens fluem através dos limites organizacionais.
        
        ![Fluxo de Mensagens](https://d2slcw3kip6qmk.cloudfront.net/marketing/pages/chart/seo/bpmn/message-flow.svg)
        
    - **Associação**: uma linha pontilhada que mostra as relações entre texto e artefatos; dados e objetos de fluxo.
        
        ![Associação](https://d2slcw3kip6qmk.cloudfront.net/marketing/pages/chart/seo/bpmn/association.svg)
        
    
    **Raias/piscina**: organizam os diferentes aspectos de um processo de negócios em um fluxograma multifuncional. Aparecem como retângulos largos.
    
    ![Raias](https://d2slcw3kip6qmk.cloudfront.net/marketing/pages/chart/seo/bpmn/swimlanes.svg)
    
    **Artefatos**: categorizam atividades e podem ser usados para incluir mais informações sobre um processo na BPMN.
    
    - **Objeto de dados**: os dados necessários para um processo. Parece um pedaço de papel com o canto superior direito dobrado para baixo.
    - **Grupo**: retângulo com cantos arredondados e com linhas tracejadas, ele agrupa diferentes atividades.
    - **Anotação de texto**: texto que fornece maiores informações.
    
    ![Artefatos](https://d2slcw3kip6qmk.cloudfront.net/marketing/pages/chart/seo/bpmn/artifacts.svg)
    

## **User Stories**

**User Stories (Histórias de Usuário)** são documentos usados em metodologias ágeis para descrever funcionalidades de uma solução. Seu principal objetivo pode ser resumido em uma palavra: **comunicar** — isto é, transmitir claramente a visão do cliente e orientar o time de desenvolvimento sobre o que deve ser construído.

A linguagem, o formato e o nível de detalhamento das User Stories devem considerar o público-alvo, geralmente composto pelo cliente e pelo time de desenvolvimento (incluindo análise, design, programação e qualidade). Como cada empresa, time e cliente possuem características próprias, não existe uma fórmula única ou regra absoluta para escrever boas histórias.

Apesar disso, há **boas práticas** que ajudam a tornar as User Stories mais claras, alinhadas e eficazes, contribuindo para a criação de soluções que realmente entreguem valor.

As boas práticas indicam que uma **User Story** deve conter dois elementos principais: **Descrição** e **Critérios de Aceitação**.

#### 1️⃣ Descrição

A descrição segue o modelo **“quem – o quê – por quê”** (role–feature–benefit), identificando:

- **Persona (quem?)**
- **Funcionalidade (o quê?)**
- **Objetivo ou benefício (por quê?)**

Exemplo:

“Como analista de crédito, quero visualizar as informações de risco do cliente, para ter assertividade na aprovação de crédito.”

Uma boa história precisa deixar clara a persona e a necessidade atendida; caso contrário, não deve ser priorizada.

Além disso, recomenda-se incluir:

- **Contextualização**: explica onde a história se encaixa no produto, ajudando todo o time a entender o cenário e a prioridade.
- **Protótipos**: auxiliam na visualização da solução e servem de apoio aos critérios de aceitação. Podem ser anexados ou referenciados por link.

Assim, a estrutura sugerida para a Descrição é:

**Contextualização + (quem, o quê, por quê) + Protótipos.**

---

#### 2️⃣ Critérios de Aceitação

São as **condições que precisam ser atendidas para que a funcionalidade seja considerada pronta e aceita pelo usuário**.

Eles se baseiam em:

- Regras de negócio
- UX
- Acessibilidade
- Segurança
- Permissões
- Outros aspectos relevantes para o desenvolvimento

Não há formato obrigatório, mas um dos mais utilizados é o modelo **orientado a cenário (Given/When/Then – Dado/Quando/Então)**, herdado do BDD, que descreve:

- O contexto,
- A ação do usuário,
- O resultado esperado.

Em resumo, uma boa User Story comunica claramente o valor da funcionalidade e define critérios objetivos para garantir que ela atenda às expectativas do usuário.

# 5. Validação e Verificação

Os conceitos de *Verificação* e *Validação* (V&V) são fundamentais para garantir a qualidade de um software. Embora sejam frequentemente confundidos, cada um tem um propósito distinto dentro do ciclo de desenvolvimento.

**Verificação** refere-se ao processo de garantir que o software foi desenvolvido corretamente em conformidade com as especificações e requisitos definidos. Essa etapa envolve atividades como revisões de código, inspeções de documentos, análise estática e testes unitários. A principal pergunta da verificação é: *“Estamos construindo o produto certo?”*.

**Validação**, por outro lado, garante que o produto final atenda às expectativas e necessidades do cliente. Nessa fase, são realizados testes funcionais, testes de aceitação e simulações em ambiente real. A pergunta central da validação é: *“Estamos construindo o produto certo para o usuário?”*.

Esse processo comumente é dividido em:

#### **Revisões:**

Buscam encontrar erros, anomalias, omissões decorrentes de todo o processo, aparecendo em qualquer estágio, podendo analisar e verificar qualquer produto decorrente do desenvolvimento do software 

#### **Prototipação**:

Criação de versões iniciais e simplificadas de um sistema antes da implementação. O seu principal objetivo é oferecer uma representação visual e interativa do que está por vir. Os protótipos representam o produto final e permitem que o cliente visualize e interaja com suas principais funcionalidades já nas fases iniciais do projeto.

#### **Teste Baseado em Requisitos e Rastreabilidade:**

Testes baseados em requisitos (RBT) validam o software contra especificações funcionais, garantindo que cada requisito seja testado. A rastreabilidade, frequentemente usando uma **Matriz de Rastreabilidade de Requisitos (RTM)**, vincula requisitos a casos de teste, facilitando a cobertura total, detecção precoce de erros e gestão de mudanças, assegurando que o produto final atenda às expectativas.

[Universidade Federal do Espírito Santo](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACYElEQVQ4jaWTz0sUcQDFP99xZsd11d3UrDXatkz6peyaHUqkQxhBRAfRIAgSEsVLUOg/YpeUrFPgQUOLMOkUdA3pB1JSax0KzVqLWtvZnZnXqS4dOviOD96Hd3gPtijTcHrUbBWy5Qa1/5gGIraN41RQG6skWR9nR10Nq/nvrK1v8mJ6HPnvSew/hWk4Pfr9T9AyBssyGMAPQvwwJAhCiiWfUtHDdmwcx+F4poUDe3bw5NlrbMsytWEoMBbFcplisYQfhlS5EeI1VWxPxGht2c3xzAESMZe19a+caK6hgoDLZzLYPwqeYtEIQekXh9M7yR5Mc6R5F9mDe0kmXFLJBj7k3vH40UM+/vzB1Wuj9PX28mhhgfptCbi78Ewnz/YK0O3bdyRJn1c/6dLFC2pp3qf5+XlNTU0pk8kqHo/rxcuXkqRC4acmbt0SknT+/DkBmpyclCTlVt7r5vi42tvbNTZ2Q0EQaG5uTtFoVE7E1aEjbbo+MiJJsgX4gQCIRCKUSiWqopVUx2JsbGyQTO5kYmKC4eFhuru7OdZ2mLXVNbL7UnzcLGMbUE11NQBNTU0sLy/jeR4DAwMUi0Xy+TxDQ0Nc6OsjUV/P02+i0jEsb3icuv8GGzCDg4N0dXXh+z4zMzP09/fT2tpKKpWio6MDYwx1ddvwQnHlwXPe5jexjCG0bYykvzuYnZ2lsbGRzs5OPM/DdV0AQgkLKIdw9N4Sr9YLOE4FgcAGdi8uLpLL5ejp6cEYgyRc12VlZQVjDOl0GhAYsDAY2/oL3voXJP33jQIMUA5FdnqJpS8FLNsiFPwGONkPGCBvqKsAAAAASUVORK5CYII=)

**O que são Testes Baseados em Requisitos (RBT)?**

- **Foco na Qualidade:** A metodologia foca em identificar e corrigir falhas de requisitos no início, antes que se tornem caros de consertar
- **Níveis de Teste:** É ideal para testes de sistema e aceitação, garantindo que o software funcione conforme o esperado.
- **Cobertura:** Garante que todos os requisitos funcionais tenham casos de teste correspondentes.

[](data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5OjcBCgoKDQwNGg8PGjclHyU3Nzc1Nzc3Nzc3Nzc3NzctLTc3Nzc1NTU3NzctNzUrNys1NzUuNTc3LTcyNTUrNy03Nf/AABEIACAAIAMBIgACEQEDEQH/xAAYAAEBAQEBAAAAAAAAAAAAAAAFBgcEA//EACsQAAEDAwMCBQQDAAAAAAAAAAECAwQABRESITFBYQYiUXGBFDKR4QcVFv/EABgBAAIDAAAAAAAAAAAAAAAAAAEEAAID/8QAGhEBAAMBAQEAAAAAAAAAAAAAAQACESEDEv/aAAwDAQACEQMRAD8A90oKxtU+0xLvniqRaw8uLDj41raHmUogHn5P4q1jxwgYCcnt0qfbtsT+4kR7kVgOqDpWleknpk47Ck1wjnmFrdjP+WVZ0Nyo1zkymSoJcZk6TgHYEEAcHFJNsBOVYGduKOtEWI7DC4v1jJjrUhLanyULST1GohXYn07U43HV5cZxUqqdlfapW2Eye+fyDMLq27MymOhOQH3RqWe4TwPnNFwrjcZSEXAyVuy9ZClObgnP244G2Nhjmj7vbZVrlfS3KO5HdUNSQ4OfY8H4rnt8qRDLojS3I+tIJ0HZX7HQ8itWonJKvyy4meMrlbJbMZlEPUwlAkAJKk6lcpyT02G2Nz2q38IeLod+ywUCNMSMlkqCgseqT19qwh58jJJJ1Dck980lYrk9EmMy2VaXG1hYPtRKGZBdbOs//9k=)

[](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAcElEQVR4AWP4//8/RZh6BgCZAkDsAMUNWDFCXgDFACCV8J/B+D8pGKwHRAKRAUyQDEMMQAYEUGBAAsiABpwKHjz4/9/BAZ8BDXgNgIMNGyg04MABkg1AeCEgAK8XKA5EiqORooSELykXEJuUBz43AgAIA1ZhBoG9vwAAAABJRU5ErkJggg==)

**Rastreabilidade de Requisitos (O "Como")**

- **Mapeamento Bidirecional:** A rastreabilidade conecta requisitos à sua implementação e verificação (casos de teste) ao longo de todo o ciclo de vida.
- **Matriz de Rastreabilidade (RTM):** Documento que cruza os Requisitos com os Casos de Teste (e bugs), facilitando a identificação de lacunas de teste (cobertura) e o impacto de mudanças.
- **Benefícios:**
    - **Cobertura:** Garante que 100% dos requisitos sejam testados.
    - **Análise de Impacto:** Facilita a identificação de quais testes precisam ser reexecutados quando um requisito muda.
    - **Gestão de Mudanças:** Permite rastrear a origem e a evolução de cada requisito.
        
        [Visure Solutions](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAC4klEQVRIia1VS08TURT+7m2nNH0MoQUfsRKwIYRuQBHYQKMGH4EYtKRudGV0Y2L8IcYf4SskaFDDI5oYF4gbXegGMSGNDSSNxsxgy0wZUuYeF7XDTDu1BPySSc7ce+6553zn3HOgKMoUEWn0/6EpijLFiEgDEIQdQhA4Z/uSndAZEZHLxv7gchF3bB5Udoli9wL7JucMpRKRphFMEw11qqOwgZFpCsdBIYiKRajTz7C19AH+wQG0pNPwRCMOnVIuB/XhY5QyGcjpScijo4AkOXTAOYOVc9MUFXFz8b3IxLvLX/sJoU5PC/s+maZQHj4SGV+zyMS7xffkGaF//CTIBbUU2UJkh9vAWqPQns+glMs5mSgWgSNR8GNHIdQN5F++gkWXzQav4Y1z1tTZAV9yGDC2wUJBlL6uID83D5RKVjID/f3g8U7Qzg6YHIbx+g22Vr7V5IrXJA+AFIsxOT25myg5DH12DsbqqrUW6OtF6FoaVNgEAFC+AGEYqIZ7mQIIj4zAf+kiSNPBvF6Ya+vIv7DRIEkslByBlOgB/fwFX3IYTZ0dqLbH69UwCwTQfGUCLBS0aCguLED//MXS8ScSLDg+Bqz/gJyehBSLOcsYAHdLbqXEAn29CFweBxU2wbxewNhGYWYGpqJaut62Vvjv3ERwcKjGeydF1Y9ICIIkMXlsDJ724+UoQkFsLy4hPz8P0jQyFZWM5WXIqZTzndhslXtR/WYFCEHqk6f4ff8BeKTFWvadOgmRL0CKx3Ho3l2wUIi5NUBnFdXpL+FzZ+EbOA3SdMDjAQAYb99hJ5tF89WJsnE3FhwU1VGAEOQoW1tvCt+4Dn9XlyPaarlxN/2bj+DgEJqSwxDZNYjsGqRED+QL5539x8VB7z+9t/17ohFEbt+ijUAQVNQhp1LlsmwwhJzddA8Tq/LQLN4b4OATrXJ5HYcOPtEqRutQ7D709xtFLXSuquosAN310F7lOsZVVZ39A3SzQmA54Uy3AAAAAElFTkSuQmCC)
        

**Principais Vantagens:**

1. **Aumento da Confiança:** Melhora a qualidade do produto ao garantir cobertura total dos requisitos.
2. **Redução de Custos:** Detecta defeitos de requisitos no início.
3. **Auditoria:** Facilita auditorias e conformidade, pois prova que o software atende ao que foi solicitado.

# 6. Gerenciamento de Requisitos

## Gerenciamento de mudanças

**Gerenciamento de mudanças:** é essencial porque alterações nas especificações são naturais ao longo do projeto. Para controlá-las, utiliza-se a **matriz de rastreabilidade** e um processo formal de avaliação e aprovação.

Toda solicitação de mudança deve ser documentada e incluir:

- Descrição da mudança
- Tipo (corretiva, preventiva, reparo de defeito etc.)
- Justificativa
- Impactos e benefícios esperados
- Alternativas caso não seja implementada

A análise pode ser feita por um comitê com stakeholders ou pelo gerente de projetos, dependendo do impacto da alteração. Mudanças desnecessárias devem ser descartadas ou transformadas em novos projetos, pois aumentam incertezas e riscos.

Independentemente de serem aprovadas ou não, todas as solicitações devem ser registradas e comunicadas às partes interessadas.

Quanto ao acompanhamento do projeto, planilhas podem funcionar em projetos pequenos. Porém, em projetos maiores, tornam-se inviáveis e propensas a erros, sendo recomendável o uso de ferramentas mais robustas de gestão.

## Versionamento

#### Noções básicas de Controle de Versão

O **controle de versão (VCS)** é um sistema que rastreia todas as alterações feitas no código-fonte, permitindo consultar históricos, comparar versões e reverter mudanças quando necessário. Ele funciona como uma “rede de segurança”, possibilitando que desenvolvedores experimentem sem comprometer o projeto e resolvam conflitos de forma organizada.

Além disso, cria uma **fonte única de verdade**, facilitando colaboração, revisão de código e identificação de responsáveis por alterações.

---

### Tipos de sistemas de controle de versão

- **Centralizado (CVCS):**
Um único repositório central. Todos os usuários trabalham nele.
- **Distribuído (DVCS):**
Cada desenvolvedor possui uma cópia completa do repositório, permitindo trabalho remoto e maior flexibilidade.
- **Baseado em bloqueio:**
Arquivos são bloqueados para evitar edições simultâneas conflitantes.
- **Otimista:**
Permite edições simultâneas e resolve conflitos no momento da integração.

---

### Benefícios do controle de versão

- **Qualidade:** incentiva revisão por pares, rastreamento detalhado e correção precoce de bugs.
- **Aceleração:** permite trabalho paralelo (branching e merging) e rápida recuperação de versões anteriores.
- **Visibilidade:** aumenta transparência e organização, integrando código com tarefas e marcos do projeto.

---

### Principais sistemas de controle de versão

- **Git:** distribuído, open source e o mais popular atualmente.
- **Subversion (SVN):** centralizado, simples e amplamente utilizado.
- **Mercurial:** distribuído, com interface intuitiva e bom suporte a branching e merging.

## Matriz de Rastreabilidade de Requisitos

### O que é Matriz de Rastreabilidade de Requisitos (RTM)?

A **Matriz de Rastreabilidade de Requisitos (RTM)** é um documento ou ferramenta estruturada usada para **garantir que todos os requisitos de um projeto sejam rastreados e validados ao longo de todo o ciclo de vida do desenvolvimento**. Ela liga cada requisito a artefatos relacionados — como especificações de design, tarefas de desenvolvimento, casos de teste e entregas — de forma organizada.

---

### Por que a RTM é importante?

A RTM:

- **Assegura que nenhum requisito seja negligenciado.**
- **Melhora a visibilidade e responsabilidade** do projeto para todas as partes interessadas.
- **Facilita a análise de impacto de mudanças**, ajudando a entender como alterações nos requisitos afetam outras partes do projeto.
- **Ajuda a garantir conformidade com padrões da indústria**, especialmente em setores altamente regulamentados, como aeroespacial, saúde e automotivo.
- **Aprimora a verificação e validação do produto**, porque relaciona requisitos a seus testes correspondentes.

---

### Como a RTM funciona

A RTM **mapeia relações entre requisitos e outros artefatos** — por exemplo:

- Requisitos → casos de teste
- Requisitos → tarefas de desenvolvimento
- Requisitos → entregas finais

Assim, ela atua como um repositório central que permite aos times monitorar o progresso, verificar se os requisitos estão sendo cumpridos e identificar lacunas ou inconsistências.

---

### Conceito de rastreabilidade de requisitos

Rastreabilidade de requisitos é o processo de **vincular requisitos aos artefatos relacionados**, assegurando que cada requisito seja acompanhado desde sua origem até sua implementação e teste. A RTM é a ferramenta que documenta e organiza esses vínculos.

---

### Tipos de rastreabilidade

A RTM suporta vários tipos de rastreabilidade:

- **Rastreabilidade futura:** liga requisitos aos seus elementos de design e testes.
- **Rastreabilidade reversa:** liga elementos de projeto de volta aos requisitos originais.
- **Rastreabilidade bidirecional:** combina rastreabilidade futura e reversa para máximo controle e cobertura.

---

### Benefícios principais

Entre as vantagens de usar uma RTM eficaz estão:

- **Maior visibilidade e clareza** sobre como os requisitos são tratados.
- **Gestão de mudanças mais eficiente.**
- **Melhor verificação e validação**, garantindo que os requisitos realmente foram implementados e testados.
- **Apoio à conformidade e auditorias.**

# MVP

O conceito de **MVP (Produto Mínimo Viável)** defende a eliminação de desperdícios. No desenvolvimento de software, o maior desperdício é investir anos em um sistema que não terá usuários. Por isso, é melhor testar rapidamente uma ideia do que gastar muitos recursos em algo incerto.

O MVP consiste em desenvolver uma versão simples do produto, com requisitos mínimos suficientes para **testar uma hipótese de negócio**. Em vez de longos levantamentos de requisitos ou pesquisas de mercado pouco confiáveis, a proposta é validar a ideia na prática.

O método Lean Startup segue o ciclo:

**Construir → Medir → Aprender**

- **Construir:** criar o MVP.
- **Medir:** disponibilizá-lo para usuários reais e coletar dados.
- **Aprender:** analisar métricas e gerar aprendizado validado.

A partir desse aprendizado, três caminhos são possíveis:

1. **Ajustar e repetir o ciclo**, refinando o MVP.
2. **Escalar o produto**, caso haja adequação ao mercado (market fit).
3. **Desistir ou pivotar**, criando um novo MVP com base no aprendizado anterior.

Um ponto crucial é evitar **métricas de vaidade** (ex.: número de visualizações), que não ajudam na tomada de decisão. O foco deve estar em **métricas acionáveis**, como taxa de conversão, valor médio de compra ou custo de aquisição de clientes.

Para produtos digitais, utilizam-se também **métricas de funil**, como:

- **Aquisição** (visitantes),
- **Ativação** (cadastros),
- **Retenção** (retorno de usuários),
- **Receita** (compras),
- **Recomendação** (indicações).

Link de um capítulo de livro de onde veio a maior parte do estudo sobre requisitos:

https://engsoftmoderna.info/cap3.html
