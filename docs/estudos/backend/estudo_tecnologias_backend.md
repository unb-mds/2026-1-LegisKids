# Estudo Tecnologias Back-end

## Estrutura do Repositório

Este documento reúne um estudo inicial sobre tecnologias utilizadas no desenvolvimento back-end, abordando linguagens de programação, frameworks, APIs REST e bancos de dados. O objetivo é apresentar opções e características para auxiliar na definição das tecnologias do projeto.

---

## 1. Escolha da Linguagem

Para a escolha da linguagem de programação a ser utilizada, foram consideradas inicialmente duas opções principais. A decisão permanece aberta para sugestões e discussão em grupo.

### Opções consideradas

- **JavaScript (Node.js):**
  Permite utilizar a mesma linguagem tanto no front-end quanto no back-end, facilitando a integração entre as camadas da aplicação. É uma excelente escolha para desenvolvimento de APIs e aplicações em tempo real. Como desvantagem, pode ser menos estruturado e gerar maior complexidade na organização do código.

- **Python:**
  Possui um grande ecossistema de bibliotecas e frameworks voltados para APIs, inteligência artificial e automação. É amplamente utilizado devido à sua simplicidade e facilidade de aprendizado. Como ponto negativo, pode apresentar desempenho inferior em alguns cenários quando comparado a outras opções.

### Material complementar

https://www.youtube.com/watch?v=2OP8ubKnyfo

---

## 2. Frameworks Back-end

Os frameworks auxiliam na organização e aceleração do desenvolvimento da aplicação, oferecendo estruturas prontas e recursos úteis.

### Frameworks analisados

- **Django (Python):**
  Framework completo, com muitos recursos integrados e forte foco em segurança. Em contrapartida, pode ser mais pesado e menos flexível para projetos menores.

- **Flask (Python):**
  Framework leve, simples e altamente flexível. Permite maior controle sobre a arquitetura, porém exige configuração manual de diversos componentes.

- **Express (Node.js):**
  Framework minimalista e rápido para criação de APIs e aplicações web. Oferece bastante liberdade, mas exige maior atenção dos desenvolvedores em relação à estrutura e segurança.

---

## 3. APIs REST

As APIs REST são um padrão de comunicação entre sistemas que utilizam o protocolo HTTP para troca de informações. Elas permitem que diferentes aplicações, como front-end e back-end, se comuniquem de forma simples e organizada.

Nesse modelo, os dados são tratados como recursos (por exemplo, usuários ou produtos) e manipulados por meio dos principais métodos HTTP:

- **GET:** Buscar dados
- **POST:** Criar novos dados
- **PUT/PATCH:** Atualizar dados existentes
- **DELETE:** Remover dados

As informações geralmente são transmitidas no formato **JSON**, que é leve e fácil de interpretar.

Esse tipo de API é amplamente utilizado por ser simples, padronizado e independente de tecnologia, facilitando a integração entre diferentes sistemas.

### Material complementar

https://www.youtube.com/watch?v=S7MduKwvVGk&t=239s

---

## 4. Bancos de Dados

Existem dois principais tipos de bancos de dados: **relacionais** e **não relacionais**. Cada um possui vantagens e desvantagens que devem ser consideradas conforme as necessidades do projeto.

### Tipos de bancos de dados

- **Relacional:**
  Possui estrutura organizada em tabelas, maior integridade dos dados e é ideal para sistemas tradicionais que exigem consistência. Como desvantagem, apresenta menor flexibilidade para mudanças estruturais.

- **Não relacional (NoSQL):**
  Oferece maior flexibilidade e facilidade de escalabilidade, sendo ideal para dados variáveis ou aplicações distribuídas. Em contrapartida, pode oferecer menor controle sobre a consistência dos dados.

### Material complementar

https://www.youtube.com/watch?v=--s6RQ3Me3A

---

## Objetivo

Garantir uma visão geral das principais tecnologias back-end disponíveis, permitindo comparar alternativas e apoiar a escolha das ferramentas mais adequadas para o desenvolvimento do projeto.