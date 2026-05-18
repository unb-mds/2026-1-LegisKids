# Decisão de Hospedagem do Banco de Dados

## Objetivo

Definir a melhor estratégia de hospedagem para o banco de dados do projeto, considerando:

- uso de PostgreSQL
- estrutura com menos de 10 tabelas relacionais
- baixo volume de requisições (projeto acadêmico)
- crescimento de dados incerto

---

## Opções analisadas

### Hospedagem local

Banco de dados executado na máquina de um integrante do grupo.

#### Vantagens

- custo zero
- simplicidade de configuração
- bom para desenvolvimento inicial

#### Desvantagens

- baixa disponibilidade (depende da máquina estar ligada)
- acesso externo limitado
- maior risco de perda de dados
- difícil colaboração entre integrantes
- não adequado para integração com frontend remoto

---

### Hospedagem em nuvem

Banco de dados hospedado em um serviço cloud, acessível via internet. Opções consideradas: Neon, Supabase e AWS RDS.

---

## Análise técnica

### Características do projeto

O banco terá menos de 10 tabelas relacionais, dados estruturados sem arquivos pesados, baixo volume de acessos simultâneos e uso acadêmico não crítico. Isso implica baixo consumo de CPU e armazenamento, com necessidade maior de simplicidade do que de escala.

---

### Estimativa de armazenamento

O projeto consumirá dados da API de projetos de lei da Câmara dos Deputados, filtrando os relacionados à segurança da criança na internet. Cada registro pode conter ID, título, ementa, texto/justificativa, autor, data, situação e temas.

#### Estimativa por registro

| Campo | Tamanho estimado |
| --- | --- |
| ID + metadados | ~100 bytes |
| Título (ementa curta) | ~200 bytes |
| Ementa detalhada | ~500 bytes |
| Texto (justificativa) | ~2 KB a 10 KB |
| Outros campos | ~200 bytes |

Total por registro: conservador ~3 KB, médio ~5 KB, alto ~10 KB.

#### Quantidade estimada de dados

| Cenário | Nº de projetos | Tamanho total |
| --- | --- | --- |
| Pequeno | 500 | ~2,5 MB |
| Médio | 2.000 | ~10 MB |
| Grande | 10.000 | ~50 MB |
| Muito grande | 50.000 | ~250 MB |

O número de projetos relacionados ao tema é limitado. Mesmo armazenando milhares de registros, o banco ficará bem abaixo de 0,5 GB, com crescimento lento e previsível.

#### Fatores de risco

O tamanho pode crescer significativamente caso o sistema armazene o texto completo dos projetos, histórico de versões ou dados redundantes da API sem filtro.

#### Estratégias para otimizar armazenamento

- armazenar apenas campos relevantes, evitando duplicação
- salvar apenas resumo/ementa quando possível
- normalizar autores, temas, etc. em tabelas separadas
- usar `TEXT` (PostgreSQL já otimiza internamente)

#### Conclusão da estimativa

O banco de dados provavelmente ficará entre **5 MB e 100 MB** na maioria dos cenários — bem abaixo do limite de 500 MB, com margem de segurança confortável.

---

### Opções em nuvem

#### Neon (PostgreSQL serverless)

- plano gratuito: 0,5 GB de armazenamento, compute limitado, escala para zero quando ocioso
- custo adicional: ~$0,35 por GB extra/mês
- vantagens: custo inicial zero, escalabilidade automática, PostgreSQL puro, ideal para uso intermitente
- desvantagens: possível latência inicial (cold start), limite inicial de armazenamento

---

#### Supabase

- plano gratuito: ~500 MB de banco
- plano pago: ~$25/mês
- vantagens: fácil integração, inclui autenticação e backend prontos
- desvantagens: menos controle, custo fixo mais alto ao escalar, pode ser excessivo para o escopo do projeto

---

#### AWS RDS

- plano: ~750h gratuitas por 1 ano, ~20 GB de armazenamento
- após free tier: ~$10–15/mês mínimo
- vantagens: alta confiabilidade, controle total, padrão de mercado
- desvantagens: configuração mais complexa, custo maior desde o início, não escala para zero

---

### Comparação

| Critério | Neon | Supabase | AWS RDS |
| --- | --- | --- | --- |
| Custo inicial | $0 | $0 | ~$0–10 |
| Armazenamento | 0,5 GB | ~0,5 GB | 20 GB |
| Escala para zero | Sim | Não | Não |
| Complexidade | Baixa | Muito baixa | Média |
| Controle | Médio | Médio | Alto |
| Indicado para | Acadêmico/MVP | MVP completo | Produção |

---

## Análise de risco

O principal risco identificado é o crescimento do banco além de 0,5 GB. A probabilidade é baixa, considerando as poucas tabelas, dados estruturados e baixo volume de uso. O custo adicional por armazenamento extra é pequeno e a migração é simples por se tratar de PostgreSQL padrão.

Mitigações:

- monitorar tamanho do banco periodicamente
- limpar dados desnecessários (logs, temporários)
- migrar ou escalar caso necessário

---

## Decisão final

**PostgreSQL em nuvem via Neon.**

### Justificativa

- custo zero inicial, ideal para projeto acadêmico
- baixa complexidade de configuração e uso
- escalabilidade adequada ao crescimento do projeto
- não cobra quando o sistema está ocioso
- flexibilidade para migrar facilmente para outras soluções PostgreSQL caso necessário

### Estratégia de uso

- **desenvolvimento local** — PostgreSQL local ou Docker
- **integração e testes** — Neon
- **produção acadêmica** — Neon

### Plano de contingência

Caso o banco ultrapasse os limites ou surjam novas necessidades:

- expandir armazenamento no Neon (baixo custo)
- ou migrar para Supabase (mais recursos) ou AWS RDS (maior robustez)

---

## Conclusão

Para um projeto acadêmico com poucas tabelas, baixo volume de requisições e crescimento incerto, o PostgreSQL em nuvem via Neon oferece o melhor equilíbrio entre custo, simplicidade e escalabilidade.