# Definição da Arquitetura do Sistema

# Monitoramento Legislativo: Proteção de Crianças na Internet

Este documento tem como objetivo analisar de forma inicial a arquitetura mais adequada para o sistema, considerando que os requisitos ainda estão em fase de definição.

A análise é baseada no seguinte estudo:

https://www.notion.so/Estudo-Arquitetura-de-Software-32d40c012af180298e76e6ef7712b3ed?pvs=21

---

## Objetivos do sistema

- Coletar dados de APIs legislativas
- Classificar proposições por tema utilizando NLP
- Gerar indicadores e análises
- Exibir dashboards interativos

---

# Avaliação das arquiteturas

## Arquitetura Monolítica

Todo o sistema é desenvolvido como uma única aplicação, incluindo API, regras de negócio, processamento de IA e acesso a dados.

### Vantagens

- Simples de implementar
- Fácil deploy
- Ideal para equipes pequenas
- Menor custo de infraestrutura
- Mais rápida para iniciar o projeto

### Desvantagens

- Escalabilidade limitada
- Pode se tornar difícil de manter em sistemas grandes
- Alto acoplamento se mal estruturado

---

## Arquitetura de Microsserviços

O sistema é dividido em serviços independentes, como:

- Coleta de dados
- Processamento e NLP
- Análise de dados
- Interface

### Vantagens

- Alta escalabilidade
- Independência entre serviços
- Flexibilidade tecnológica

### Desvantagens

- Alta complexidade
- Maior custo de infraestrutura
- Comunicação entre serviços mais difícil
- Não indicado para projetos pequenos

---

## Arquitetura MVC

Separação em três componentes:

- Model: dados e regras de negócio
- View: interface do usuário
- Controller: controle de requisições

### Vantagens

- Estrutura organizada
- Separação clara de responsabilidades
- Fácil manutenção
- Muito utilizada em aplicações web

### Desvantagens

- Controllers podem ficar sobrecarregados
- Não define arquitetura completa do sistema

---

## Arquitetura em Camadas

Divisão do sistema por níveis de responsabilidade:

- Interface (Frontend)
- Aplicação (Controllers)
- Negócio (Services)
- Dados (Repositories)
- Infraestrutura (Banco e APIs)

### Vantagens

- Alta organização
- Boa separação de responsabilidades
- Fácil manutenção
- Amplamente utilizada em sistemas reais

### Desvantagens

- Pode gerar dependência entre camadas
- Possível impacto de performance se mal aplicada

---

# Decisão de arquitetura

O sistema será desenvolvido como um **monólito estruturado em camadas**, utilizando conceitos do padrão **MVC** para organização da interface e controle.

---

## Monolito

O sistema será implementado como uma única aplicação, pois:

- o escopo do projeto não exige microsserviços
- a complexidade seria desnecessária neste momento
- facilita desenvolvimento e manutenção

---

## Arquitetura em camadas

O sistema será dividido nas seguintes camadas:

1. Interface (Frontend)
   - Dashboards
   - Filtros
   - Visualização de dados

2. Aplicação (Controller)
   - Recebe requisições
   - Controla o fluxo da aplicação

3. Negócio (Service)
   - Regras de negócio
   - Processamento de dados
   - NLP e classificação

4. Dados (Repository)
   - Acesso ao banco de dados
   - Consumo de APIs externas

5. Infraestrutura
   - Banco de dados
   - Configurações
   - Integrações externas

Fluxo de dependência:

Interface → Controller → Service → Repository → Banco de Dados

---

## Aplicação do MVC

O sistema seguirá o padrão MVC adaptado ao contexto web:

- Model: Services + Repositories
- View: Frontend
- Controller: Camada de controle de requisições

---

### Fluxo MVC

- Usuário interage com a interface (View)
- Frontend envia requisição
- Controller recebe a requisição
- Service processa a lógica de negócio
- Repository acessa os dados
- Resultado retorna ao Controller
- Controller responde à View

---

## Estrutura do sistema

### Backend

- Controller: recebe e direciona requisições
- Service: regras de negócio e processamento de IA
- Repository: acesso a dados e APIs externas
- Infraestrutura: banco de dados e configurações

### Frontend

- Dashboards
- Filtros
- Visualização de dados

---

## Conclusão

A arquitetura escolhida combina um modelo **monolítico com organização em camadas**, garantindo:

- simplicidade de desenvolvimento
- boa organização interna
- facilidade de manutenção
- compatibilidade com o escopo do projeto

Essa abordagem equilibra estrutura profissional com baixo nível de complexidade, sendo adequada para a fase atual do sistema.