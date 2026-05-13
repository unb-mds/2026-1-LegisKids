# Estudo sobre Fluxo de Dados
Este documento tem o intuito de reavaliar a ideia atual do Fluxo de Dados do sistema, propor pelo menos 3 alternativas, e decidir a melhor para nosso projeto.

Primeiramente iremos falar sobre os dados das proposições, e depois sobre os dados salvos para cada usuário (proposições favoritas, histórico, etc).

# Proposições

## Atual

Ainda não possuíamos uma ideia concreta sobre o que das proposições, e nem como armazenar no banco de dados do sistema, o que impacta diretamente na performance, escalabilidade e confiabilidade do sistema, especialmente na construção de dashboards e análises.

## Ideia 1: salvar o ID de cada projeto de lei

Periodicamente, o sistema irá salvar o ID de cada proposição, e na hora de rodar alguma parte do site, pedirá para consumir as APIs da Câmara dos Deputados do Brasil para cada ID, e, assim, mostrar as informações.

### Prós:

- Baixo uso de armazenamento no banco de dados
- Implementação simples
- Dados sempre atualizados diretamente da fonte oficial

### Contras:

- Alta latência (múltiplas requisições por carregamento)
- Forte dependência da disponibilidade da API externa
- Possibilidade de rate limiting
- Baixa escalabilidade
- Experiência do usuário prejudicada em dashboards
- Alto custo de requisições conforme o sistema cresce

## Ideia 2: salvar o Json da API em nosso banco de dados

Contando com o consumo periódico da API, buscando novas proposições, o sistema salvará organizadamente cada JSON em nosso banco de dados.

### Prós:

- Independência da API em tempo de execução
- Redução de latência no frontend
- Facilidade de implementação (armazenamento direto)
- Permite auditoria dos dados originais

### Contras:

- Dificuldade em realizar consultas eficientes (JSON não otimizado para análise)
- Maior complexidade para gerar dashboards
- Possível redundância de dados
- Crescimento desorganizado do banco
- Necessidade de processamento adicional para extrair insights

## Ideia 3: pegar o JSON, tratá-lo de acordo com nossas necessidades, e salvá-lo no banco de dados

Contando com o consumo periódico da API, buscando novas proposições, o sistema pegará organizadamente cada JSON, tratará os dados, normalizará os campos relevantes (como tipo, data, tema), classificará o conteúdo com ajuda de IA (por exemplo, identificar temas como “proteção de crianças na internet”), e, só assim, irá salvá-lo de forma estruturada no banco de dados.

### Prós:

- Alta performance para consultas e dashboards
- Dados já preparados para análise
- Independência da API externa em tempo de execução
- Melhor escalabilidade
- Possibilidade de criar métricas e agregações rapidamente
- Estrutura organizada e consistente
- Permite uso de cache (ex: Redis) para otimização adicional

### Contras:

- Maior complexidade de implementação
- Necessidade de definir modelo de dados antecipadamente
- Custo de processamento (tratamento + classificação)
- Necessidade de manutenção do pipeline de dados (ETL)
- Possíveis erros na classificação automática (IA)

## Conclusão

A Ideia 1 apresenta baixa complexidade, porém não atende aos requisitos de performance e escalabilidade do sistema.

A Ideia 2 melhora a independência e a disponibilidade dos dados, mas ainda não resolve de forma eficiente a necessidade de análise e construção de dashboards.

A Ideia 3, apesar de mais complexa, é a abordagem mais adequada para o projeto, pois permite transformar os dados brutos em informações estruturadas e prontas para análise, garantindo melhor desempenho, escalabilidade e experiência do usuário.

Portanto, recomenda-se a adoção da **Ideia 3**, possivelmente combinada com o armazenamento do JSON original para fins de auditoria e reprocessamento futuro.

### Explicação da decisão

#### 1. Dashboards exigem dados prontos

No protótipo tem:

- gráfico de proposições por ano
- gráfico por tema

Precisamos de dados assim:

```
{
  "ano":2024,
  "total":1523
}
```

E não:

```
[lista gigante de proposições]
```

Isso só é possível com dados tratados (Ideia 3).

#### 2. Classificação por tema (IA)

O tema:

> “proteção de crianças na internet”
> 

A API não vem pronta com isso.

Com isso:

- ou classificamos manualmente (inviável)
- ou usamos a IA (Ideia 3)

#### 3. Filtros rápidos

No protótipo tem filtros tipo:

- ano
- tipo (PL, PEC…)
- tema

Se usarmos:

- JSON bruto → lento
- API em tempo real → pior ainda

Banco estruturado → resposta instantânea

#### 4. Escalabilidade

A API oferece **muitos dados** (proposições, deputados, votações etc.)

Conforme o sistema cresce:

- Ideia 1 quebra primeiro
- Ideia 2 começa a sofrer
- Ideia 3 escala bem

## Fluxo dos Dados

No consumo periódico da API:

1. API (dados abertos)
2. Backend consome periodicamente
3. Trata dados (ETL)
4. Classifica com IA
5. Salva estruturado no banco
6. Frontend consome dados prontos

A API **não é baseada em “última atualização global”**, mas oferece algo equivalente:

- **tramitação = mudança no projeto**

> **“o que se movimentou recentemente?”**
> 

#### Usaremos:

`listarProposicoesTramitadasNoPeriodo`

Exemplo mental:

```
buscar tudo que mudou entre:
01/05/2026 → 02/05/2026
```

Isso dará:

- projetos que foram movimentados
- ou seja: **projetos atualizados**

### Fluxo ideal

1. Salva último timestamp:

```
ultima_verificacao = ontem 00:00
```

1. Roda job:

```
buscar tramitações entre ontem e hoje
```

1. Para cada ID retornado:
- chama `ObterProposicaoPorID`
- atualiza no banco

## Limitação importante

A API NÃO garante:

- um campo tipo `dataAtualizacao` global
- nem um endpoint tipo:
    
    ```
    /proposicoes?updated_after=...
    ```
    

Ou seja:

- você depende da **tramitação como proxy de mudança**

Isso significa que nem toda mudança será capturada perfeitamente

(ex: correção de texto sem nova tramitação)

Mas na prática, **para dashboards e análise política, isso é suficiente.**

# Dados dos Usuários (favoritos, histórico, etc)

## Atual

Ainda não havia uma definição clara de como os dados específicos de cada usuário seriam armazenados no sistema.

A ideia inicial poderia levar a armazenar listas diretamente dentro do usuário (ex: favoritos, histórico), o que não é adequado para bancos relacionais e pode gerar problemas de performance e escalabilidade.

## Ideia 1: armazenar listas diretamente no usuário (JSON ou arrays)

Cada usuário teria campos contendo listas, como:

```
user: {
  id: 1,
  favoritos: [123, 456],
  historico: [111, 222]
}
```

### Prós:

- Implementação simples
- Fácil de entender conceitualmente
- Menor número de tabelas

### Contras:

- Difícil de consultar (ex: “quem favoritou tal proposição?”)
- Baixa performance em buscas e filtros
- Dificuldade de indexação
- Estrutura pouco escalável
- Problemas ao crescer o volume de dados
- Não segue boas práticas de bancos relacionais

## Ideia 2: tabelas separadas para cada tipo de dado do usuário (modelo relacional)

Criar tabelas específicas para representar relações entre usuário e proposições:

Exemplo:

- `users`
- `favoritos`
- `historico`
- `notificacoes`

### Prós:

- Alta performance em consultas
- Fácil de escalar
- Permite indexação eficiente
- Facilita queries complexas (ex: recomendações, análises)
- Estrutura organizada e consistente
- Segue boas práticas de bancos relacionais
- Permite crescimento futuro do sistema

### Contras:

- Maior número de tabelas
- Implementação um pouco mais complexa
- Necessidade de entender relações (joins)

## Ideia 3: abordagem híbrida (relacional + otimizações específicas)

Utilizar o modelo relacional como base (Ideia 2), mas com otimizações:

- tabelas relacionais para favoritos, histórico e notificações
- uso de cache (ex: Redis) para dados mais acessados
- possibilidade de armazenar alguns dados derivados (ex: contagem de favoritos)

### Prós:

- Melhor performance geral do sistema
- Redução de carga no banco principal
- Escalabilidade elevada
- Flexibilidade para otimizações futuras
- Ideal para sistemas com dashboards e alta interação

### Contras:

- Maior complexidade arquitetural
- Necessidade de gerenciar cache
- Maior esforço de manutenção

## Conclusão

A Ideia 1, apesar de simples, não é adequada para um sistema que precisa escalar e realizar consultas eficientes.

A Ideia 2 resolve corretamente o problema utilizando um modelo relacional, sendo suficiente para a maioria dos casos e alinhada com boas práticas de desenvolvimento.

A Ideia 3 adiciona uma camada de otimização, sendo mais indicada conforme o sistema cresce e passa a exigir maior performance.

**Usaremos a ideia 2.**

### Estrutura

- `proposicoes` → armazena todas as proposições tratadas e normalizadas do sistema
- `users` → armazena os dados dos usuários
- `favoritos` → representa a relação entre usuários e proposições favoritas
- `historico` → registra as interações dos usuários com as proposições
- `notificacoes` → armazena eventos de atualização relevantes para os usuários

As tabelas se relacionam por meio de chaves estrangeiras (`user_id` e `proposicao_id`), seguindo um modelo relacional que evita duplicação de dados e garante escalabilidade.