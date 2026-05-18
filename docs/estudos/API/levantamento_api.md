# Estudo de APIs – Monitoramento Legislativo

## Visão geral

Este documento apresenta o levantamento e análise das APIs e fontes de dados disponíveis para o sistema de monitoramento legislativo, bem como a decisão de arquitetura de dados adotada no projeto.

---

## Conteúdo principal

### Fontes de dados

#### Coleta primária

##### Câmara dos Deputados

- Fonte principal do projeto  
- Fornece dados completos sobre proposições e tramitações  
- Documentação disponível via Swagger e Dados Abertos  

##### Senado Federal

- Fonte complementar de dados legislativos  
- Pode ser utilizado futuramente para expansão do sistema  

---

### Enriquecimento e consolidação

#### LexML

- Não deve ser utilizado como fonte primária  
- Utilizado apenas para:
  - normalização de dados  
  - deduplicação  
  - resolução de documentos jurídicos  

---

### Publicação oficial

#### Diário Oficial da União (DOU)

- Fonte oficial de atos normativos  
- Utilizado como referência de validação  
- Disponível via catálogo de APIs governamentais  

---

### Descoberta de dados

#### Portal dados.gov.br

- Utilizado apenas como suporte  
- Permite:
  - descoberta de datasets  
  - identificação de organizações  
  - busca por categorias e tags  

---

## Decisão do projeto

Apesar da existência de múltiplas fontes de dados, para viabilizar o projeto dentro do prazo:

Será utilizada como fonte principal apenas a API da Câmara dos Deputados.

---

## O que a API da Câmara oferece

A API cobre os principais dados necessários para o sistema:

- Proposições  
- Tramitações  
- Autores  
- Comissões e órgãos  
- Temas  

---

## Endpoints principais

- /api/v2/proposicoes  
- /api/v2/proposicoes/{id}  
- /api/v2/proposicoes/{id}/tramitacoes  
- /api/v2/proposicoes/{id}/autores  
- /api/v2/proposicoes/{id}/temas  
- /api/v2/orgaos  
- /api/v2/orgaos/{id}  

---

## Formato e atualização

A API da Câmara fornece:

- API REST  
- Formatos suportados:
  - JSON  
  - CSV  
  - XML  
  - XLSX  
  - ODS  
- Atualização diária dos dados principais  

---

## Cobertura da solução

A API cobre:

- proposições  
- tramitações  
- autores  
- comissões  
- temas  

---

## Limitações e riscos

A API não cobre completamente:

- Senado Federal  
- Publicações oficiais no DOU  
- Classificação específica sobre proteção digital de crianças  

### Pontos de atenção

- escopo limitado à Câmara dos Deputados  
- classificação temática genérica  
- possíveis mudanças na API  
- necessidade de filtros e regras próprias  

---

## Conclusão

A API da Câmara dos Deputados atende adequadamente o escopo inicial do projeto e será utilizada como fonte principal de dados, permitindo a coleta estruturada de informações sobre:

- proposições  
- tramitações  
- autores  
- comissões  