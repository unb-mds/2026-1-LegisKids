# Estudo sobre integração de IA no projeto

## 1. Definição da Tecnologia (Stack)

- **Modelo Escolhido:** Google Gemini 1.5 Flash
- **Forma de Uso:** API via SDK oficial (`google-generativeai`)
- **Objetivo da IA:** Triagem e classificação de dados brutos (filtragem)
- **Justificativa:** APIs governamentais retornam uma grande massa de dados. A IA atuará como um filtro para identificar quais projetos de lei (PLs) são relacionados ao tema “Proteção de Crianças na Internet”, separando-os de conteúdos genéricos ou irrelevantes.

## 2. Ponto de Integração no Sistema

A IA será o **Portão de Qualidade (Quality Gate)** do sistema.

- **Localização arquitetural:** camada de `services` (ex: `app/services/filter_service.py`)
- **Momento da integração:** após a coleta dos dados brutos da API governamental
- **Resultado:** apenas dados aprovados pela IA serão armazenados no PostgreSQL e exibidos no sistema

## 3. Estrutura de Código e Módulos

- `app/services/filter_service.py`: lógica de filtragem; recebe uma lista de PLs e retorna apenas os relevantes
- `app/models.py`: armazena apenas itens filtrados, otimizando o banco de dados
- `.env`: armazenamento seguro da chave de acesso à API do Gemini

## 4. Fluxo Básico de Funcionamento (Entrada → Filtragem → Saída)

### 1. Entrada (Raw Data)
O sistema coleta diariamente projetos de lei da API governamental, contendo dados de diversos temas.

### 2. Processamento (AI Filtering)

O `filter_service` envia o título e a ementa do PL para a IA.

**Prompt de filtragem:**

> Analise o projeto abaixo. Ele contém medidas diretas sobre proteção de menores em ambiente digital, crimes cibernéticos contra crianças ou segurança de dados infantis? Responda apenas SIM ou NÃO.

A IA atua como um classificador binário.

### 3. Saída (Curated Content)

- **NÃO:** o dado é descartado
- **SIM:** o dado é salvo e exibido no sistema

## 5. Gestão de Cotas e Limites

Para lidar com o limite de requisições da API do Gemini (15 RPM no plano gratuito), serão aplicadas estratégias de otimização:

- Pré-filtragem por keywords: reduz o volume enviado à IA
- Batch processing: envio de múltiplos registros em uma única requisição
- Persistência de decisões: evitar reprocessar PLs já analisados

## Síntese

A IA será usada como um filtro inteligente dentro da camada de serviços, funcionando como um mecanismo de triagem entre os dados brutos da API e os dados realmente relevantes para o sistema. Isso reduz ruído, melhora a qualidade da informação exibida e mantém o sistema focado no objetivo principal do projeto.