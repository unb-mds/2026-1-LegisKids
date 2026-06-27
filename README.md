# LegisKids

### Sistema de Monitoramento de Proposições Legislativas

> Projeto desenvolvido pelo Squad-08 na disciplina de Métodos de Desenvolvimento de Software (MDS) — FCTE/UnB, semestre 2026/1.

---

## Descrição Geral

O **LegisKids** é um sistema web desenvolvido para monitorar, analisar e facilitar o acesso a proposições legislativas no Brasil. A plataforma busca tornar o acompanhamento legislativo mais acessível, organizado e compreensível para a sociedade.

---

## Protótipo

Acesse o protótipo interativo no Figma:

[Visualizar protótipo](https://embed.figma.com/design/9Gdfmyo1J2oWtnAmUYd1Vl/Prototipo-Site-MDS?node-id=0-1&t=diM94hTSvFm83IMz-1&embed-host=notion&footer=false&theme=system)

---

## Integrantes da Equipe

Squad-08 MDS 2026/1 – FCTE/UnB

<table>
  <tr>
    <td align="center">
      <img src="docs/assets/images/team/caio-bechepeche.jpg" width="100px;" alt="Caio Bechepeche Mota"/><br />
      <sub><b>Caio Bechepeche Mota</b></sub><br />
      <a href="https://github.com/CaioMota16">GitHub</a>
    </td>
    <td align="center">
      <img src="docs/assets/images/team/renan-curione.jpg" width="100px;" alt="Renan Curione de Castro"/><br />
      <sub><b>Renan Curione de Castro</b></sub><br />
      <a href="https://github.com/thatsrenan">GitHub</a>
    </td>
    <td align="center">
      <img src="docs/assets/images/team/italo-lacerda.jpg" width="100px;" alt="Ítalo Lacerda Martins"/><br />
      <sub><b>Ítalo Lacerda Martins</b></sub><br />
      <a href="https://github.com/italo-lm">GitHub</a>
    </td>
    <td align="center">
      <img src="docs/assets/images/team/luis-henrique.jpg" width="100px;" alt="Luís Henrique Luna de Arruda"/><br />
      <sub><b>Luís Henrique Luna de Arruda</b></sub><br />
      <a href="https://github.com/Donnk61">GitHub</a>
    </td>
    <td align="center">
      <img src="docs/assets/images/team/arthur-palhares.jpg" width="100px;" alt="Arthur Palhares Ferreira Silva"/><br />
      <sub><b>Arthur Palhares Ferreira Silva</b></sub><br />
      <a href="https://github.com/arthurpalhares1">GitHub</a>
    </td>
  </tr>
</table>

---

## Objetivo do Sistema

O sistema busca:

* Facilitar o acesso à informação legislativa
* Apoiar análises de proposições legislativas
* Organizar informações públicas de forma acessível
* Auxiliar no monitoramento de mudanças relevantes

---

## Contexto

O grande volume de dados legislativos e a complexidade das informações dificultam o acompanhamento de proposições por parte da sociedade.

O LegisKids surge como uma solução para:

* Centralizar informações legislativas
* Organizar dados de maneira estruturada
* Facilitar o acompanhamento de proposições
* Tornar o acesso à informação mais acessível

---

## Tecnologias Utilizadas

| Camada         | Tecnologia                   |
| -------------- | ---------------------------- |
| Front-end      | Vue 3 + Vite                 |
| Roteamento     | Vue Router 4                 |
| Estado global  | Pinia                        |
| Gráficos       | Chart.js 4                   |
| Back-end       | Python + Flask               |
| Banco de Dados | PostgreSQL                   |
| ORM            | SQLAlchemy                   |
| Documentação   | MkDocs + Material for MkDocs |
| Prototipação   | Figma                        |

---

## Estrutura do Projeto

```text
docs/                -> documentação do projeto
src/
  backend/           -> Flask + SQLAlchemy (backend)
  frontend/          -> Vue 3 + Vite (frontend SPA)
openspec/            -> especificações e mudanças
scripts/             -> scripts auxiliares
```

---

## Como Executar o Frontend

### Pré-requisitos

* Node.js 18+
* npm 9+

### 1. Instalar dependências

```bash
cd src/frontend
npm install
```

### 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
# Edite .env se o backend estiver em outra porta/host
```

### 3. Iniciar o servidor de desenvolvimento

```bash
npm run dev
# Disponível em http://localhost:5173
```

### 4. Build de produção

```bash
npm run build
# Saída em src/frontend/dist/
```

---

## Como Executar a Documentação

### Pré-requisitos

Certifique-se de possuir:

* Python 3.10+
* pip
* Git

---

### 1. Clonar o repositório

```bash
git clone https://github.com/unb-mds/2026-1-LegisKids.git
cd 2026-1-LegisKids
```

---

### 2. Criar ambiente virtual

#### Linux/Mac

```bash
python -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar o banco de dados

O projeto suporta dois modos de banco de dados:

#### Banco local com Docker (desenvolvimento diário)

Suba o PostgreSQL usando o `docker-compose.yml` do projeto:

```bash
docker compose up -d
```

Aguarde o container ficar saudável (alguns segundos) antes de continuar. Para verificar:

```bash
docker compose ps
```

Para parar:

```bash
docker compose down
```

> O volume `legiskids_db_data` persiste os dados entre reinicializações. Para apagar tudo e começar do zero: `docker compose down -v`

#### Banco Neon (homologação e testes remotos)

Obtenha a connection string no painel do [Neon](https://neon.tech) e use-a no `.env` local.

### 6. Configurar variáveis de ambiente

Copie o arquivo de exemplo e edite com suas credenciais:

```bash
cp .env.example .env
```

Exemplo para banco local Docker:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/legiskids
FLASK_APP=src/backend/app.py
FLASK_ENV=development
SECRET_KEY=troque-por-uma-chave-secreta-longa-e-aleatoria
```

Exemplo para banco Neon:

```env
DATABASE_URL=postgresql://usuario:senha@host.neon.tech/legiskids?sslmode=require
FLASK_APP=src/backend/app.py
FLASK_ENV=development
SECRET_KEY=troque-por-uma-chave-secreta-longa-e-aleatoria
```

> A connection string real do Neon deve ser obtida no painel e **nunca commitada**.

### 7. Executar as migrations e popular o banco

> **Pré-requisito:** o banco configurado na `DATABASE_URL` do seu `.env` precisa estar acessível antes de executar os comandos abaixo.
> - Se usar banco local Docker: execute `docker compose up -d` primeiro.
> - Se usar Neon: certifique-se de que a `DATABASE_URL` no `.env` aponta para o Neon com `?sslmode=require`.

Aplique o schema:

```bash
python -m flask --app src/backend/app.py db upgrade
```

Popule o banco com dados iniciais:

```bash
python scripts/seed.py
```

> **Status de validação:**
> - **Banco local Docker** — testado e validado: migrations aplicadas e seed executado com sucesso (17 partidos inseridos).
> - **Banco Neon** — requer troca temporária do `DATABASE_URL` conforme instruções abaixo.

#### Testando no banco Neon

Para aplicar o schema e popular o banco remoto no Neon, troque temporariamente o `DATABASE_URL` no seu `.env` pela connection string do Neon (obtida no painel do [Neon](https://neon.tech)):

```env
# Temporário — para testar no Neon
DATABASE_URL=postgresql://<usuario>:<senha>@<host>.neon.tech/<banco>?sslmode=require&channel_binding=require
```

### 7. Documentação do banco de dados

A documentação completa do schema está disponível em [`docs/db/schema.md`](docs/db/schema.md), incluindo:
- Diagrama Entidade-Relacionamento (ERD)
- Descrição de cada tabela, colunas, tipos e constraints
- Relacionamentos e decisões de design

O código-fonte do ERD (editável no [dbdiagram.io](https://dbdiagram.io)) está em [`docs/db/erd.dbml`](docs/db/erd.dbml).

---

### 8. Executar as migrations (se houver)
Execute as migrations e o seed:

```bash
python -m flask --app src/backend/app.py db upgrade
python scripts/seed.py
```

### 9. Iniciar o servidor

```text
http://127.0.0.1:8000
```

---

## Subindo o banco com Docker

Pré-requisito: [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado.

```bash
# 1. Copie o arquivo de variáveis de ambiente
cp .env.example .env

# 2. Suba o banco
docker compose up -d

# 3. Aplique as migrations
flask db upgrade

# 4. Popule com dados iniciais (opcional)
python scripts/seed.py

# 5. Pare o banco quando terminar
docker compose down
```

> As credenciais são lidas do `.env`. Nenhuma senha está hardcoded no `docker-compose.yml`.

---

## Contribuindo

1. Faça um fork do projeto

2. Crie uma branch:

```bash
git checkout -b feature/nome-da-feature
```

3. Commit suas alterações:

```bash
git commit -m "feat: adiciona nova funcionalidade"
```

4. Faça push:

```bash
git push origin feature/nome-da-feature
```

5. Abra um Pull Request

---

## Licença

Este projeto está licenciado sob a licença MIT.

Consulte o arquivo `LICENSE` para mais informações.

---

## Equipe

Projeto desenvolvido na disciplina de Métodos de Desenvolvimento de Software (MDS) — Faculdade de Ciências e Tecnologias em Engenharia (FCTE/UnB), semestre 2026/1.