# LegisKids

### Sistema de Monitoramento de Proposições Legislativas

> Projeto desenvolvido pelo Squad-08 na disciplina de Métodos de Desenvolvimento de Software (MDS) — FGA/UnB, semestre 2026/1.

---

## Descrição Geral

O **LegisKids** é um sistema web desenvolvido para monitorar, analisar e facilitar o acesso a proposições legislativas no Brasil. A plataforma permite que usuários busquem leis, acompanhem mudanças e entendam o impacto de decisões legislativas de forma clara e acessível.

---

## Protótipo

Acesse o protótipo interativo no Figma:
[Visualizar protótipo](https://embed.figma.com/design/9Gdfmyo1J2oWtnAmUYd1Vl/Prototipo-Site-MDS?node-id=0-1&t=diM94hTSvFm83IMz-1&embed-host=notion&footer=false&theme=system)

---

## Integrantes da Equipe

Squad-08 MDS 2026/1 – FGA/UnB

<table>
  <tr>
    <td align="center">
      <img src="docs/assets/images/team/caio-bechepeche.jpg" width="100px;" alt="Caio Bechepeche Mota"/><br />
      <sub><b>Caio Bechepeche Mota</b></sub><br />
      <a href="https://github.com/CaioMota16">GitHub</a>
    </td>
    <td align="center">
      <img src="docs/assets/images/team/renan-curione.jpg" width="auto;" height="100px;" alt="Renan Curione de Castro"/><br />
      <sub><b>Renan Curione de Castro</b></sub><br />
      <a href="https://github.com/thatsrenan">GitHub</a>
    </td>
    <td align="center">
      <img src="docs/assets/images/team/italo-lacerda.jpg" width="auto;" height="100px;" alt=" Ítalo Lacerda Martins"/><br />
      <sub><b>Italo Lacerda Martins</b></sub><br />
      <a href="https://github.com/italo-lm">GitHub</a>
    </td>
    <td align="center">
      <img src="docs/assets/images/team/luis-henrique.jpg" width="auto;" height="100px;" alt="Luís Henrique Luna de Arruda"/><br />
      <sub><b>Luís Henrique Luna de Arruda</b></sub><br />
      <a href="https://github.com/Donnk61">GitHub</a>
    </td>
    <td align="center">
      <img src="docs/assets/images/team/arthur-palhares.jpg" width="auto;" height="100px;" alt="Arthur Palhares Ferreira Silva"/><br />
      <sub><b>Arthur Palhares Ferreira Silva</b></sub><br />
      <a href="https://github.com/arthurpalhares1">GitHub</a>
    </td>
  </tr>
</table>
---

## Objetivo do Sistema

O objetivo do sistema é fornecer uma ferramenta que:

- Facilite o acesso à informação legislativa
- Apoie a análise de leis e propostas
- Permita o monitoramento de mudanças relevantes
- Auxilie usuários na compreensão do impacto de proposições

---

## Contexto

A grande quantidade de informações legislativas disponíveis e a complexidade dos dados tornam difícil para cidadãos e analistas acompanharem mudanças nas leis.

O LegisKids surge como uma solução para:

- Centralizar dados legislativos
- Organizar e classificar informações automaticamente
- Tornar o acompanhamento mais acessível e eficiente

---

## Tecnologias Utilizadas

| Camada | Tecnologia |
|---|---|
| Front-end | HTML, CSS, JavaScript, Next.js |
| Back-end | Python (Flask) |
| Consumo de API | Fetch API |
| Banco de Dados | PostgreSQL |
| Prototipação | Figma |

---

## Como Executar o Projeto

### Pré-requisitos

Certifique-se de ter instalado:

- [Node.js](https://nodejs.org/) (versão 18 ou superior)
- [npm](https://www.npmjs.com/)
- [Python](https://www.python.org/) (versão 3.10 ou superior)
- [PostgreSQL](https://www.postgresql.org/)
- [Git](https://git-scm.com/)

---

### 1. Clonar o repositório

```bash
git clone https://github.com/unb-mds/2026-1-LegisKids.git
cd 2026-1-LegisKids
```

### 2. Criar um ambiente virtual Python

```bash
python -m venv venv
```

### 3. Ativar o ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependências Python

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

```bash
flask run
```

Ou alternativamente:

```bash
python app.py
```

### 10. Acessar no navegador

```
http://localhost:3000
```

> **Atenção:** Certifique-se de que o PostgreSQL está em execução antes de iniciar a aplicação.

---

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature:
   ```bash
   git checkout -b feature/nome-da-feature
   ```
3. Commit suas mudanças:
   ```bash
   git commit -m 'feat: adiciona nova feature'
   ```
4. Faça o push para a branch:
   ```bash
   git push origin feature/nome-da-feature
   ```
5. Abra um Pull Request descrevendo suas mudanças

---

## Licença

Este projeto está licenciado sob a **Licença MIT** — uma das licenças de código aberto mais permissivas e amplamente adotadas.

Isso significa que qualquer pessoa pode **usar, copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender** cópias deste software livremente, desde que o aviso de copyright e a permissão original sejam mantidos nas cópias distribuídas.

O software é fornecido **"como está"**, sem garantias de qualquer natureza. Os autores não se responsabilizam por danos decorrentes de seu uso.

Consulte o arquivo [LICENSE](./LICENSE) para o texto completo da licença.

---

## Equipe

Desenvolvido como parte do projeto de **Métodos de Desenvolvimento de Software (MDS)** da Universidade de Brasília (UnB) — Faculdade do Gama (FGA), semestre 2026/1.