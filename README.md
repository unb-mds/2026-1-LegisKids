# 2026-1-Squad08 — LegisKids

# LegisKids
### Sistema de Monitoramento de Proposições Legislativas

---

## Descrição Geral

O LegisKids é uma plataforma web desenvolvida para monitorar, organizar e analisar proposições legislativas da Câmara dos Deputados do Brasil, com foco em temas relacionados à proteção de crianças e adolescentes no ambiente digital.

O sistema coleta dados legislativos automaticamente, trata as informações recebidas da API oficial da Câmara e disponibiliza funcionalidades de busca, filtros, visualização de indicadores e classificação inteligente das proposições.

---

## Objetivo do Sistema

O projeto tem como objetivo:

- Facilitar o acesso à informação legislativa
- Permitir o acompanhamento de proposições relevantes
- Auxiliar análises políticas e sociais
- Organizar grandes volumes de dados legislativos
- Tornar o conteúdo legislativo mais acessível e compreensível

---

## Contexto

Atualmente, acompanhar mudanças legislativas no Brasil é uma tarefa complexa devido:

- ao grande volume de proposições;
- à dificuldade de busca e filtragem;
- à linguagem técnica utilizada;
- à dispersão das informações.

O LegisKids surge como uma solução para centralizar e organizar essas informações de forma acessível, moderna e inteligente.

---

## Tecnologias Utilizadas

### Front-end
- HTML5
- CSS3
- JavaScript
- Fetch API

### Back-end
- Python
- Flask

### Banco de Dados
- PostgreSQL
- SQLAlchemy
- psycopg

### Inteligência Artificial
- Google Gemini API (`gemini-1.5-flash`)

### Ferramentas
- Git
- GitHub
- MkDocs
- Figma

---

## Protótipo

Acesse o protótipo interativo no Figma:

https://www.figma.com/design/9Gdfmyo1J2oWtnAmUYd1Vl/Prototipo-Site-MDS?node-id=0-1&t=GijhYnyynvgDqCSG-1

---

## Como Executar o Projeto

### Pré-requisitos

Certifique-se de possuir instalado:

- Python 3.11+
- PostgreSQL
- Git

---

### 1. Clonar o repositório

```bash
git clone https://github.com/unb-mds/2026-1-Squad08.git
cd 2026-1-Squad08
```

---

### 2. Criar ambiente virtual

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 4. Configurar o PostgreSQL

Crie o banco de dados:

```sql
CREATE DATABASE legiskids;
```

---

### 5. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
FLASK_APP=app.py
FLASK_ENV=development

DATABASE_URL=postgresql://postgres:sua_senha@localhost:5432/legiskids

GOOGLE_API_KEY=sua_chave_google_gemini
```

---

### 6. Executar o projeto

```bash
flask run
```

ou

```bash
python app.py
```

---

### 7. Acessar a aplicação

O sistema estará disponível em:

```txt
http://127.0.0.1:5000
```

---

## Estrutura do Projeto

```txt
backend/
├── auth/
├── controllers/
├── services/
├── repositories/
├── models/
├── routes/
├── ai/
└── config/

frontend/
├── css/
├── js/
└── pages/

docs/
```

---

## Funcionalidades Principais

- Coleta automática de proposições legislativas
- Integração com API da Câmara dos Deputados
- Busca e filtros avançados
- Dashboard de indicadores
- Classificação automática utilizando IA
- Histórico de alterações
- Sistema de autenticação
- Visualização detalhada de proposições
- Exportação de dados

---

## Integrantes da Equipe

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
      <img src="docs/assets/images/team/italo-lacerda.jpg" width="100px;" alt="Italo Lacerda Martins"/><br />
      <sub><b>Italo Lacerda Martins</b></sub><br />
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

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature

```bash
git checkout -b feature/nova-feature
```

3. Faça commit das alterações

```bash
git commit -m "feat: adiciona nova feature"
```

4. Envie para o repositório remoto

```bash
git push origin feature/nova-feature
```

5. Abra um Pull Request

---

## Status do Projeto

Projeto em desenvolvimento.

---

## Licença

Projeto acadêmico desenvolvido para a disciplina Métodos de Desenvolvimento de Software (MDS) da Universidade de Brasília (UnB).
