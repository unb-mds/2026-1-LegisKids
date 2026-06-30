# Guia de Contribuição — LegisKids

Obrigado por considerar contribuir com o **LegisKids**.

Este projeto foi desenvolvido na disciplina de Métodos de Desenvolvimento de Software (MDS) da FCTE/UnB e busca promover um ambiente colaborativo, organizado e acessível para desenvolvimento open source.

---

## Código de Conduta

Ao contribuir com este projeto, você concorda em seguir o nosso `CODE_OF_CONDUCT.md`.

---

## Estrutura do Projeto

```text
docs/           -> documentação do projeto
src/            -> código-fonte da aplicação
openspec/       -> especificações e mudanças
scripts/        -> scripts auxiliares
```

---

## Fluxo de Desenvolvimento

O projeto utiliza um fluxo baseado em GitFlow simplificado.

### Branches principais

| Branch    | Objetivo                                |
| --------- | --------------------------------------- |
| `main`    | versão estável do projeto               |
| `develop` | integração contínua das funcionalidades |

### Branches auxiliares

```text
feature/*
fix/*
refactor/*
docs/*
hotfix/*
chore/*
```

---

## Como Contribuir

### 1. Fork do repositório

Realize um fork do projeto no GitHub.

---

### 2. Clone do repositório

```bash
git clone <url-do-seu-fork>
cd 2026-1-LegisKids
```

---

### 3. Sincronize a branch `develop`

Antes de iniciar uma nova funcionalidade, atualize sua branch local:

```bash
git checkout develop
git pull origin develop
```

---

### 4. Criação da branch

Crie uma branch seguindo o padrão:

```text
tipo/numero-issue-nome-curto
```

Exemplos:

```text
feature/12-login
fix/34-validacao-api
docs/21-guia-instalacao
```

Exemplo de criação:

```bash
git checkout -b docs/165-documentacao-oss
```

---

### 5. Realize as alterações

Implemente sua funcionalidade, correção ou documentação.

---

### 6. Commit das alterações

Os commits devem seguir o padrão:

```text
tipo: descrição curta
```

Exemplos:

```text
feat: adiciona autenticação JWT
fix: corrige erro na validação
docs: atualiza documentação da API
```

---

## Prefixos Oficiais

| Prefixo      | Uso                 |
| ------------ | ------------------- |
| `feat`       | nova funcionalidade |
| `fix`        | correção de bug     |
| `refactor`   | refatoração         |
| `docs`       | documentação        |
| `style`      | formatação          |
| `test`       | testes              |
| `chore`      | manutenção          |
| `infra`      | infraestrutura      |
| `devops`     | CI/CD e deploy      |
| `management` | gestão de processos |

---

## Processo de Pull Request

### 1. Envie a branch

```bash
git push origin nome-da-branch
```

---

### 2. Abra um Pull Request

O Pull Request deve ser direcionado para:

```text
develop
```

A branch `main` deve receber apenas versões estáveis.

---

## Padrão de título do PR

```text
[tipo] #numero-issue - descrição curta
```

Exemplo:

```text
[docs] #165 - adiciona documentação OSS
```

---

## Modelo de descrição do PR

```markdown
## O que foi feito?

## Por que isso foi feito?

## Como testar?

## Prints/Vídeos (se houver)

## Issue relacionada

Closes #numero
```

---

## Boas Práticas

* Nunca commitar diretamente na `main`
* Sempre utilizar branches
* Manter PRs pequenos e objetivos
* Relacionar Issues ao Pull Request
* Utilizar mensagens claras em commits
* Atualizar a documentação quando necessário

---

## Ambiente Local

O passo a passo completo de instalação está no
[README](README.md#como-executar-localmente).

### Executar API

```bash
python -m flask --app src/backend/app.py run --debug
```

### Executar documentação

```bash
python -m pip install -r requirements-docs.txt
python -m mkdocs serve
```

Antes de enviar mudanças na documentação, valide o build:

```bash
python -m mkdocs build --strict
```

### Executar frontend

```bash
cd src/frontend
npm install
npm run dev
```

### Executar testes

```bash
python -m pip install pytest
python -m pytest tests/
```

---

## Licença

Ao contribuir com este projeto, você concorda que suas contribuições serão licenciadas sob a licença MIT.
