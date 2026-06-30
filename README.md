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

## Como Executar Localmente

### Pré-requisitos

* Git
* Python 3.10+
* Node.js 18+ e npm 9+
* Acesso à `DATABASE_URL` do projeto no Neon

### 1. Clonar o repositório

```bash
git clone https://github.com/unb-mds/2026-1-LegisKids.git
cd 2026-1-LegisKids
```

### 2. Preparar o backend

Crie e ative um ambiente virtual:

#### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows (PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Instale as dependências e crie o arquivo de configuração local:

```bash
python -m pip install -r requirements.txt
cp .env.example .env
```

No Windows, use `copy .env.example .env`.

Abra o `.env` e substitua a `DATABASE_URL` vazia pela connection string
fornecida pelo responsável pelo banco:

```env
DATABASE_URL=postgresql://<usuario>:<senha>@<host>.neon.tech/<banco>?sslmode=require&channel_binding=require
```

Copie a connection string completa pelo botão **Connect** no painel do Neon ou
solicite-a ao responsável pelo banco. Ela contém credenciais e deve permanecer
somente no `.env`; nunca a publique em commits, issues ou mensagens abertas.
Preencha `GOOGLE_API_KEY` apenas se for executar a classificação automática.
O `FLASK_ENV=testing` do exemplo impede que o scheduler diário seja iniciado
por cada ambiente local conectado ao banco compartilhado.

### 3. Iniciar o backend

```bash
python -m flask --app src/backend/app.py run --debug
```

A API estará disponível em `http://127.0.0.1:5000`. Para verificar a conexão
com o banco, acesse `http://127.0.0.1:5000/health`.

> Não execute migrations ou o seed no banco compartilhado sem autorização do
> responsável pelo banco. Alterações de schema devem ser coordenadas pela
> equipe.

### 4. Iniciar o frontend

Em outro terminal, a partir da raiz do repositório:

```bash
cd src/frontend
npm install
cp .env.example .env
npm run dev
```

No Windows, use `copy .env.example .env`. A aplicação estará disponível em
`http://localhost:5173`.

Para gerar o build de produção:

```bash
npm run build
```

## Como Executar a Documentação

Com o ambiente virtual ativo, instale as dependências específicas:

```bash
python -m pip install -r requirements-docs.txt
python -m mkdocs serve
```

A documentação estará disponível em `http://127.0.0.1:8000`.

Para validar o site antes de enviar alterações:

```bash
python -m mkdocs build --strict
```

## Documentação do Banco de Dados

A documentação completa do schema está disponível em
[`docs/db/schema.md`](docs/db/schema.md), incluindo o diagrama
Entidade-Relacionamento, as tabelas, constraints e decisões de design.
O código-fonte editável do ERD está em
[`docs/db/erd.dbml`](docs/db/erd.dbml).

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
