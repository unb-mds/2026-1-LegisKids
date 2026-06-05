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
| Front-end      | HTML, CSS e JavaScript       |
| Back-end       | Python + FastAPI             |
| Servidor ASGI  | Uvicorn                      |
| Banco de Dados | PostgreSQL                   |
| ORM            | SQLAlchemy                   |
| Documentação   | MkDocs + Material for MkDocs |
| Prototipação   | Figma                        |

---

## Estrutura do Projeto

```text
docs/           -> documentação do projeto
src/            -> código-fonte da aplicação
openspec/       -> especificações e mudanças
scripts/        -> scripts auxiliares
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

---

### 4. Executar a documentação localmente

```bash
mkdocs serve
```

A documentação ficará disponível em:

```text
http://127.0.0.1:8000
```

---

## Como Executar a API

Execute:

```bash
uvicorn src.auth_api.main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

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