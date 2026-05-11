# Estudo sobre integração de IA no projeto

## 1. Definição da Tecnologia (Stack)

- **Modelo Escolhido:** Google Gemini 1.5 Flash.
- **Forma de Uso:** API via SDK oficial (`google-generativeai`).
- **Objetivo da IA:** Triagem e classificação de dados brutos (Filtragem).
- **Justificativa:** APIs governamentais retornam uma grande massa de dados. A IA atuará como um filtro de "peneira fina" para identificar quais projetos de lei (PLs) realmente tocam no tema "Proteção de Crianças na Internet", separando-os de leis genéricas ou irrelevantes.

## 2. Ponto de Integração no Sistema

A IA será o **Portão de Qualidade (Quality Gate)** do sistema.

- **Localização Arquitetural:** Dentro da camada de `services` (ex: `app/services/filter_service.py`).
- **Momento da Integração:** Ocorre logo após a coleta dos dados brutos da API do Governo. Somente os dados aprovados pelo filtro de IA serão armazenados permanentemente no PostgreSQL para exibição.

## 3. Estrutura de Código e Módulos

- **`app/services/filter_service.py`**: Contém a lógica de filtragem. Recebe uma lista de PLs e retorna apenas os que atendem aos critérios de proteção infantil.
- **`app/models.py`**: Armazena apenas os itens filtrados, otimizando o espaço do banco de dados.
- **`.env`**: Protege a chave de acesso à API do Gemini.

## 4. Fluxo Básico de Funcionamento (Entrada → Filtragem → Saída)

O fluxo de filtragem segue esta lógica:

1. **Entrada (Raw Data):** O sistema busca todos os PLs do dia. Muitos tratam de temas diversos (saúde, economia, transporte).
2. **Processamento (AI Filtering):**
    - O `filter_service` envia o título e a ementa do PL para a IA.
    - **O Prompt de Filtragem:** *"Analise o projeto abaixo. Ele contém medidas diretas sobre proteção de menores em ambiente digital, crimes cibernéticos contra crianças ou segurança de dados infantis? Responda apenas SIM ou NÃO."*
    - A IA atua como um classificador binário.
3. **Saída (Curated Content):**
    - Se **NÃO**: O dado é descartado.
    - Se **SIM**: O sistema processa o PL para exibição no site, garantindo um feed 100% focado no tema.
    - 

**Gestão de Cotas e Limites:**
Para mitigar o limite de 15 RPM (requisições por minuto) do plano gratuito do Gemini, o sistema adotará:

- **Pré-filtragem por Keywords:** Redução do volume de dados enviados à IA.
- **Batch Processing:** Envio de múltiplos registros em uma única chamada.
- **Persistência de Decisão:** Projetos já analisados são marcados no banco para evitar reprocessamento e desperdício de cota.
