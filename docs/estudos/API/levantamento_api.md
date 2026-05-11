# 📡 Estudo de APIs – Monitoramento Legislativo

## 📌 Fontes de Dados

### 🔹 Coleta Primária

#### Câmara dos Deputados
- Fonte principal para o projeto
- Fornece dados completos sobre proposições e tramitações
- Documentação: Swagger UI / Dados Abertos

#### Senado Federal
- Fonte complementar para dados legislativos

---

### 🔹 Enriquecimento e Consolidação

#### LexML
- Não deve ser fonte primária
- Usado para:
  - normalização de dados
  - deduplicação
  - resolução de documentos jurídicos

---

### 🔹 Publicação Oficial

#### Diário Oficial da União (DOU)
- Fonte prioritária para atos normativos publicados oficialmente
- API disponível no catálogo de APIs governamentais

---

### 🔹 Descoberta de Dados

#### Portal de Dados Abertos (dados.gov.br)
- Uso apenas como apoio
- Permite:
  - descobrir datasets
  - identificar organizações e grupos
  - buscar por tags

---

## ✅ Decisão para o Projeto

Apesar da existência de múltiplas APIs, para viabilizar o projeto no tempo disponível:

👉 **Será utilizada apenas a API da Câmara dos Deputados como fonte principal**

---

## 📊 O que a API da Câmara oferece

A API atende bem aos seguintes pontos:

- **Proposições**
  - Lista e detalha projetos de lei e outras proposições

- **Tramitações**
  - Acompanhamento do andamento das proposições

- **Autores**
  - Identificação dos autores das proposições

- **Comissões / Órgãos**
  - Dados sobre comissões, plenário e outros órgãos

- **Temas**
  - Classificação temática oficial

---

## 🔗 Endpoints principais

- `/api/v2/proposicoes`
- `/api/v2/proposicoes/{id}`
- `/api/v2/proposicoes/{id}/tramitacoes`
- `/api/v2/proposicoes/{id}/autores`
- `/api/v2/proposicoes/{id}/temas`
- `/api/v2/orgaos`
- `/api/v2/orgaos/{id}`

---

## ⚙️ Formato e Atualização

A API da Câmara oferece:

- API REST
- Formatos de dados:
  - JSON
  - CSV
  - XML
  - XLSX
  - ODS
- Atualização diária dos dados principais

---

## 🎯 Cobertura para a Issue

A API cobre:

- proposições  
- tramitações  
- autores  
- comissões  
- temas  

---

## ⚠️ Limitações e Riscos

A API **não cobre sozinha**:

- Senado Federal  
- Publicação oficial no DOU  
- Classificação específica sobre proteção digital de crianças  

### Pontos de atenção:

- cobre apenas a Câmara dos Deputados  
- classificação temática é genérica  
- possíveis mudanças técnicas na API  
- necessidade de filtros próprios (ex: palavras-chave)

---

## 🧠 Conclusão

A API da Câmara dos Deputados atende adequadamente o escopo do projeto e deve ser utilizada como **fonte prioritária inicial**, pois oferece dados oficiais com integração simples sobre:

- proposições  
- tramitações  
- autores  
- comissões  
