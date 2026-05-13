# Decisão de Hospedagem do Banco de Dados
## 1. Objetivo

Definir a melhor estratégia de hospedagem para o banco de dados do projeto, considerando:

- Uso de **PostgreSQL**
- Estrutura com menos de 10 **tabelas relacionais**
- **Baixo volume de requisições** (projeto acadêmico)
- **Crescimento de dados incerto**

## 2. Opções Analisadas

### 2.1 Hospedagem Local

**Descrição:**

Banco de dados executado na máquina de um integrante do grupo.

**Vantagens:**

- Custo zero
- Simplicidade de configuração
- Bom para desenvolvimento inicial

**Desvantagens:**

- Baixa disponibilidade (depende da máquina estar ligada)
- Acesso externo limitado
- Maior risco de perda de dados
- Difícil colaboração entre integrantes
- Não adequado para integração com frontend remoto

### 2.2 Hospedagem em Nuvem (PostgreSQL)

**Descrição:**

Banco de dados hospedado em um serviço cloud, acessível via internet.

**Opções consideradas:**

- Neon (PostgreSQL serverless)
- Supabase (PostgreSQL + backend)
- AWS RDS (PostgreSQL gerenciado)

## 3. Análise Técnica – Banco SQL em Nuvem

### 3.1 Características do Projeto

O banco de dados terá:

- menos de 10 tabelas relacionais
- Dados estruturados (sem arquivos pesados)
- Baixo volume de acessos simultâneos
- Uso acadêmico (não crítico)

Isso implica:

- Baixo consumo de CPU
- Baixo consumo de armazenamento (inicialmente)
- Necessidade maior de simplicidade do que de escala

## 3.2 Estimativa de Uso de Armazenamento

O projeto irá consumir dados da **API de projetos de lei da Câmara dos Deputados**, filtrando aqueles relacionados à **segurança da criança na internet**.

### Estrutura esperada dos dados

Cada projeto de lei normalmente contém:

- ID
- Título (ementa)
- Descrição/ementa detalhada
- Texto/justificativa (às vezes longo)
- Autor(es)
- Data
- Situação
- Tags/temas

Isso significa que os registros não são pequenos — principalmente por causa de **campos de texto**.

### Estimativa por registro

| Campo | Tamanho estimado |
| --- | --- |
| ID + metadados | ~100 bytes |
| Título (ementa curta) | ~200 bytes |
| Ementa detalhada | ~500 bytes |
| Texto (justificativa) | ~2 KB a 10 KB |
| Outros campos | ~200 bytes |

**Total por registro:**

- Conservador: ~3 KB
- Médio: ~5 KB
- Alto: ~10 KB

### Quantidade estimada de dados

Nem todos os projetos da Câmara serão armazenados — apenas os relacionados ao tema.

Estimativa realista:

| Cenário | Nº de projetos | Tamanho total |
| --- | --- | --- |
| Pequeno | 500 | ~2.5 MB |
| Médio | 2.000 | ~10 MB |
| Grande | 10.000 | ~50 MB |
| Muito grande (exagerado) | 50.000 | ~250 MB |

### Considerações importantes

- O número de projetos relacionados ao tema é **limitado**
- Mesmo armazenando milhares de registros:
    - ainda fica **bem abaixo de 0.5 GB**
- O crescimento é **lento e previsível**

### Possível fator de risco

O único cenário que pode aumentar muito o tamanho:

- Armazenar **texto completo do projeto (inteiro)**
- Armazenar **histórico de versões**
- Armazenar **dados redundantes da API sem filtro**

### Estratégias para otimizar armazenamento

1. **Armazenar apenas campos relevantes**
    - evitar duplicação de dados
2. **Evitar armazenar documentos completos desnecessariamente**
    - salvar apenas resumo/ementa quando possível
3. **Normalização**
    - separar autores, temas, etc.
4. **Compressão lógica**
    - usar `TEXT` (PostgreSQL já otimiza internamente)

### Conclusão da estimativa

Mesmo considerando dados reais da Câmara:

> O banco de dados provavelmente ficará entre **5 MB e 100 MB** na maioria dos cenários.
> 

Ou seja:

- Muito abaixo do limite de **0.5 GB (500 MB)**
- Com margem de segurança confortável

## 3.3 Opções em Nuvem

### 🔹 Neon (PostgreSQL Serverless)

**Plano gratuito:**

- 0.5 GB armazenamento
- Compute limitado
- Escala para zero (sem custo quando ocioso)

**Custos adicionais:**

- ~$0.35 por GB extra/mês

**Vantagens:**

- Custo inicial zero
- Escalabilidade automática
- PostgreSQL puro (sem lock-in)
- Ideal para uso intermitente

**Desvantagens:**

- Possível latência inicial (cold start)
- Limite inicial de armazenamento

### Supabase

**Plano gratuito:**

- ~500 MB banco

**Plano pago:**

- ~$25/mês

**Vantagens:**

- Fácil integração (API pronta)
- Inclui autenticação e backend

**Desvantagens:**

- Menos controle
- Custo fixo mais alto ao escalar
- Pode ser excessivo para o escopo do projeto

### AWS RDS

**Plano:**

- ~750h gratuitas por 1 ano
- ~20 GB armazenamento

**Após free tier:**

- ~$10–15/mês mínimo

**Vantagens:**

- Alta confiabilidade
- Controle total
- Padrão de mercado

**Desvantagens:**

- Configuração mais complexa
- Custo maior desde o início
- Não escala para zero

## 3.4 Comparação

| Critério | Neon | Supabase | AWS RDS |
| --- | --- | --- | --- |
| Custo inicial | $0 | $0 | ~$0–10 |
| Armazenamento | 0.5 GB | ~0.5 GB | 20 GB |
| Escala p/ zero | Sim | Não | Não |
| Complexidade | Baixa | Muito baixa | Média |
| Controle | Médio | Médio | Alto |
| Indicado p/ | Acadêmico/MVP | MVP completo | Produção |

## 4. Análise de Risco

### Risco identificado

- Crescimento do banco além de **0.5 GB**

### Probabilidade

- **Baixa**, considerando:
    - Poucas tabelas
    - Dados estruturados
    - Baixo volume de uso

Motivo:

- O custo adicional é muito pequeno
- Migração é simples (PostgreSQL padrão)

### Mitigações

1. **Monitorar tamanho do banco**
2. **Limpar dados desnecessários (logs, temporários)**
3. **Migrar ou escalar caso necessário**

## 5. Decisão Final

**Escolha:** PostgreSQL em nuvem utilizando **Neon**

## 6. Justificativa

A decisão foi baseada nos seguintes pontos:

1. **Custo zero inicial**
    - Ideal para projeto acadêmico
2. **Baixa complexidade**
    - Fácil de configurar e usar
3. **Escalabilidade adequada**
    - Cresce conforme necessário
4. **Uso eficiente para baixa demanda**
    - Não cobra quando o sistema está ocioso
5. **Flexibilidade futura**
    - Pode migrar facilmente para outras soluções PostgreSQL

## 7. Estratégia de Uso

- **Desenvolvimento local:** PostgreSQL local (ou Docker)
- **Integração e testes:** Neon
- **Produção acadêmica:** Neon

## 8. Plano de Contingência

Caso o banco ultrapasse limites ou surjam novas necessidades:

- Expandir armazenamento (baixo custo)
- Ou migrar para:
    - Supabase (mais recursos)
    - AWS RDS (maior robustez)

## 9. Conclusão

Para um projeto acadêmico com:

- Poucas tabelas
- Baixo volume de requisições
- Crescimento incerto

> A utilização de PostgreSQL em nuvem via Neon oferece o melhor equilíbrio entre **custo, simplicidade e escalabilidade**.
>