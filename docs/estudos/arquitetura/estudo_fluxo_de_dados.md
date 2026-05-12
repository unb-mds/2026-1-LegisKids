# Estudo sobre Fluxo de Dados

Este documento reavalia a ideia atual do fluxo de dados do sistema, propõe alternativas e define a melhor abordagem para o projeto.

O estudo está dividido em duas partes: dados das proposições e dados dos usuários (favoritos, histórico, etc.).

---

## Proposições

### Situação atual

Ainda não havia uma ideia concreta sobre como armazenar os dados das proposições no banco, o que impacta diretamente a performance, escalabilidade e confiabilidade do sistema, especialmente na construção de dashboards e análises.

---

### Ideia 1 — salvar apenas o ID de cada proposição

Periodicamente, o sistema salvaria o ID de cada proposição e, ao carregar qualquer parte do site, consumiria as APIs da Câmara dos Deputados para cada ID e exibiria as informações.

#### Prós

- baixo uso de armazenamento no banco de dados
- implementação simples
- dados sempre atualizados diretamente da fonte oficial

#### Contras

- alta latência (múltiplas requisições por carregamento)
- forte dependência da disponibilidade da API externa
- possibilidade de rate limiting
- baixa escalabilidade
- experiência do usuário prejudicada em dashboards
- alto custo de requisições conforme o sistema cresce

---

### Ideia 2 — salvar o JSON da API diretamente no banco

Com consumo periódico da API, o sistema salvaria cada JSON recebido diretamente no banco de dados.

#### Prós

- independência da API em tempo de execução
- redução de latência no frontend
- facilidade de implementação
- permite auditoria dos dados originais

#### Contras

- dificuldade em realizar consultas eficientes (JSON não otimizado para análise)
- maior complexidade para gerar dashboards
- possível redundância de dados
- crescimento desorganizado do banco
- necessidade de processamento adicional para extrair insights

---

### Ideia 3 — tratar o JSON e salvar estruturado no banco

Com consumo periódico da API, o sistema pegaria cada JSON, trataria os dados, normalizaria os campos relevantes (tipo, data, tema), classificaria o conteúdo com IA (por exemplo, identificar o tema "proteção de crianças na internet") e só então salvaria de forma estruturada no banco.

#### Prós

- alta performance para consultas e dashboards
- dados já preparados para análise
- independência da API externa em tempo de execução
- melhor escalabilidade
- possibilidade de criar métricas e agregações rapidamente
- estrutura organizada e consistente
- permite uso de cache (ex: Redis) para otimização adicional

#### Contras

- maior complexidade de implementação
- necessidade de definir modelo de dados antecipadamente
- custo de processamento (tratamento + classificação)
- necessidade de manutenção do pipeline de dados (ETL)
- possíveis erros na classificação automática (IA)

---

### Conclusão

A Ideia 1 apresenta baixa complexidade, porém não atende aos requisitos de performance e escalabilidade do sistema.

A Ideia 2 melhora a independência e disponibilidade dos dados, mas ainda não resolve de forma eficiente a necessidade de análise e construção de dashboards.

A Ideia 3, apesar de mais complexa, é a abordagem mais adequada, pois transforma dados brutos em informações estruturadas e prontas para análise, garantindo melhor desempenho, escalabilidade e experiência do usuário.

**Adotaremos a Ideia 3**, possivelmente combinada com o armazenamento do JSON original para fins de auditoria e reprocessamento futuro.

#### Por que a Ideia 3 é a escolha certa

**Dashboards exigem dados prontos.** O protótipo prevê gráficos de proposições por ano e por tema. Isso exige dados agregados como `{ "ano": 2024, "total": 1523 }`, não listas brutas de proposições — o que só é possível com dados tratados.

**Classificação por tema exige IA.** A API não retorna o tema "proteção de crianças na internet" automaticamente. Classificar manualmente é inviável; a IA resolve isso na Ideia 3.

**Filtros rápidos exigem banco estruturado.** O protótipo prevê filtros por ano, tipo (PL, PEC) e tema. Com JSON bruto ou API em tempo real, a resposta seria lenta. Com banco estruturado, a resposta é instantânea.

**Escalabilidade.** Conforme o sistema cresce, a Ideia 1 quebra primeiro, a Ideia 2 começa a sofrer, e a Ideia 3 escala bem.

---

### Fluxo dos dados

No consumo periódico da API:

```
API (dados abertos)
↓
Backend consome periodicamente
↓
Trata dados (ETL)
↓
Classifica com IA
↓
Salva estruturado no banco
↓
Frontend consome dados prontos
```

A API não oferece um endpoint de "última atualização global", mas oferece algo equivalente: a **tramitação como proxy de mudança**. O que se movimentou recentemente é o que foi atualizado.

Utilizaremos `listarProposicoesTramitadasNoPeriodo`. Exemplo:

```
buscar tudo que mudou entre 01/05/2026 e 02/05/2026
```

#### Fluxo ideal

1. Salvar o último timestamp de verificação:

```
ultima_verificacao = ontem 00:00
```

2. Rodar o job:

```
buscar tramitações entre ontem e hoje
```

3. Para cada ID retornado, chamar `ObterProposicaoPorID` e atualizar no banco.

---

### Limitação importante

A API não garante um campo `dataAtualizacao` global nem um endpoint do tipo `/proposicoes?updated_after=...`. O sistema depende da tramitação como proxy de mudança, o que significa que nem toda alteração será capturada perfeitamente (exemplo: correção de texto sem nova tramitação). Na prática, para dashboards e análise política, isso é suficiente.

---

## Dados dos usuários (favoritos, histórico, etc.)

### Situação atual

Ainda não havia uma definição clara de como os dados específicos de cada usuário seriam armazenados. A ideia inicial de armazenar listas diretamente no usuário não é adequada para bancos relacionais e pode gerar problemas de performance e escalabilidade.

---

### Ideia 1 — armazenar listas diretamente no usuário

Cada usuário teria campos contendo listas:

```
user: {
  id: 1,
  favoritos: [123, 456],
  historico: [111, 222]
}
```

#### Prós

- implementação simples
- fácil de entender conceitualmente
- menor número de tabelas

#### Contras

- difícil de consultar (ex: "quem favoritou tal proposição?")
- baixa performance em buscas e filtros
- dificuldade de indexação
- estrutura pouco escalável
- não segue boas práticas de bancos relacionais

---

### Ideia 2 — tabelas separadas por tipo de dado (modelo relacional)

Criar tabelas específicas para representar relações entre usuário e proposições:

- `users`
- `favoritos`
- `historico`
- `notificacoes`

#### Prós

- alta performance em consultas
- fácil de escalar
- permite indexação eficiente
- facilita queries complexas (recomendações, análises)
- estrutura organizada e consistente
- segue boas práticas de bancos relacionais
- permite crescimento futuro do sistema

#### Contras

- maior número de tabelas
- implementação um pouco mais complexa
- necessidade de entender relações (joins)

---

### Ideia 3 — abordagem híbrida (relacional + cache)

Utilizar o modelo relacional como base (Ideia 2), com otimizações:

- tabelas relacionais para favoritos, histórico e notificações
- cache (ex: Redis) para dados mais acessados
- possibilidade de armazenar dados derivados (ex: contagem de favoritos)

#### Prós

- melhor performance geral
- redução de carga no banco principal
- escalabilidade elevada
- flexibilidade para otimizações futuras

#### Contras

- maior complexidade arquitetural
- necessidade de gerenciar cache
- maior esforço de manutenção

---

### Conclusão

A Ideia 1 não é adequada para um sistema que precisa escalar e realizar consultas eficientes.

A Ideia 2 resolve corretamente o problema com modelo relacional, sendo suficiente para a maioria dos casos e alinhada com boas práticas de desenvolvimento.

A Ideia 3 adiciona uma camada de otimização, mais indicada conforme o sistema cresce.

**Adotaremos a Ideia 2.**

#### Estrutura das tabelas

- `proposicoes` — armazena todas as proposições tratadas e normalizadas
- `users` — armazena os dados dos usuários
- `favoritos` — representa a relação entre usuários e proposições favoritas
- `historico` — registra as interações dos usuários com as proposições
- `notificacoes` — armazena eventos de atualização relevantes para os usuários

As tabelas se relacionam por meio de chaves estrangeiras (`user_id` e `proposicao_id`), seguindo um modelo relacional que evita duplicação de dados e garante escalabilidade.