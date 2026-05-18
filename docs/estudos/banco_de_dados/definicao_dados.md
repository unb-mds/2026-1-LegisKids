# Identificação e Documentação dos Dados do Sistema
# Objetivo

Este documento define todos os dados que deverão ser coletados, armazenados e utilizados pelo sistema de análise legislativa sobre segurança da criança na internet.

O sistema utilizará a API pública da Câmara dos Deputados como fonte principal de dados.

O objetivo é garantir:

- armazenamento eficiente;
- ausência de dados redundantes;
- compatibilidade com os dashboards definidos;
- baixo custo computacional;
- estrutura simples e relacional.

# Objetivos do Armazenamento

O banco de dados deverá permitir:

- monitoramento de projetos de lei;
- análise temporal;
- análise política;
- análise de tramitação;
- análise de conteúdo.

Como o sistema terá limite aproximado de 200 MB, apenas dados realmente necessários serão persistidos.

# Dashboards que Dependem dos Dados

| Dashboard | Tipo |
| --- | --- |
| Panorama Geral | visualização inicial |
| Evolução Temporal | análise temporal |
| Análise Política | análise partidária e regional |
| Tramitação Legislativa | acompanhamento legislativo |
| Análise de Conteúdo | análise textual simplificada |

Os dados armazenados foram definidos prioritariamente para suportar os dashboards classificados como Must, mantendo compatibilidade parcial com dashboards classificados como Should e Could.

# Entidades Principais do Sistema

Após análise dos dashboards e da API, foram definidas 4 entidades principais:

| Entidade | Finalidade |
| --- | --- |
| Proposição | armazenar projetos de lei |
| Autor | armazenar deputados autores |
| Partido | armazenar partidos políticos |
| Tramitação | armazenar andamento legislativo |

# Entidade: Proposição

## Objetivo

Armazenar informações principais dos projetos de lei.

## Endpoint Utilizado

```
GET /proposicoes
```

## Campos Necessários

| Campo | Tipo | Justificativa |
| --- | --- | --- |
| id | inteiro | identificador único da proposição |
| siglaTipo | texto | identificar tipo da proposição |
| numero | inteiro | número oficial do projeto |
| ano | inteiro | análises temporais |
| ementa | texto | análise de conteúdo |
| dataApresentacao | data | gráficos temporais |
| descricaoSituacao | texto | status atual da proposição |
| idAutor | inteiro | relacionamento com autor principal |

## Observação

Embora uma proposição possa possuir múltiplos autores, o sistema armazenará apenas o autor principal da proposição para simplificar a modelagem relacional e reduzir complexidade.

# Entidade: Partido

## Objetivo

Permitir agrupamentos e análises partidárias.

## Endpoint Utilizado

```
GET /partidos
```

## Campos Necessários

| Campo | Tipo | Justificativa |
| --- | --- | --- |
| id | inteiro | identificador do partido |
| sigla | texto | exibição simplificada |
| nome | texto | exibição completa |

# Entidade: Tramitação

## Objetivo

Armazenar andamento legislativo das proposições.

## Endpoint Utilizado

```
GET /proposicoes/{id}/tramitacoes
```

## Campos Necessários

| Campo | Tipo | Justificativa |
| --- | --- | --- |
| idProposicao | inteiro | vínculo com proposição |
| dataHora | data/hora | análise temporal |
| descricaoSituacao | texto | situação legislativa |
| descricaoTramitacao | texto | histórico simplificado |
| siglaOrgao | texto | identificação de comissão ou órgão |

# Estratégia de Armazenamento

Para evitar crescimento excessivo do banco:

- apenas tramitações relevantes serão persistidas;
- não serão armazenados documentos completos;
- não serão armazenadas mídias;
- não serão armazenadas votações detalhadas;
- não serão armazenados anexos;
- não serão armazenados textos integrais das proposições.

# Relacionamento Entre Entidades

## Estrutura Relacional

### Proposição → Partido

Uma proposição está relacionada a um partido político.

Relacionamento:

- muitos para um.

### Proposição → Tramitação

Uma proposição possui várias tramitações.

Relacionamento:

- um para muitos.

# Dados Derivados Calculados pelo Sistema

Alguns dados poderão ser calculados internamente sem necessidade de armazenamento permanente.

| Dado | Origem |
| --- | --- |
| quantidade por ano | dataApresentacao |
| projetos ativos | descricaoSituacao |
| ranking de autores | agregação |
| projetos por partido | agregação |
| média mensal | cálculo temporal |
| distribuição por status | agregação |
| projetos por UF | agregação |

Isso evita redundância e reduz espaço no banco.

# Estratégias para Evitar Redundância

O sistema adotará as seguintes práticas:

- utilização de IDs relacionais entre entidades;
- evitar repetição de dados partidários;
- não duplicar informações retornadas pela API;
- calcular métricas dinamicamente;
- armazenar apenas informações utilizadas nos dashboards;
- evitar armazenamento de dados históricos desnecessários.

# Justificativa Técnica

A estrutura proposta foi escolhida porque:

- atende todos os dashboards classificados como Must;
- mantém compatibilidade com dashboards Should e Could;
- utiliza poucos dados;
- reduz complexidade;
- facilita consultas SQL;
- mantém baixo consumo de armazenamento;
- é adequada para PostgreSQL;
- simplifica manutenção futura;
- permite expansão futura do sistema.

O sistema não necessita de Big Data, processamento distribuído ou infraestrutura complexa, sendo suficiente uma arquitetura relacional simples.

# Conclusão

Os dados definidos neste documento são suficientes para suportar os dashboards acadêmicos do sistema sem desperdício de armazenamento ou complexidade desnecessária.

As entidades escolhidas:

- Proposição;
- Partido;
- Tramitação;

permitem:

- monitoramento legislativo;
- análise temporal;
- análise política;
- acompanhamento de tramitação;
- análise textual simplificada.

A estrutura relacional proposta é simples, eficiente e adequada ao escopo acadêmico do projeto, respeitando o limite de armazenamento e evitando dados redundantes.