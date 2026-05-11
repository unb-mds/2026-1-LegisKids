# 2026-1-Squad08
# Nome do projeto
### Sistema de Monitoramento de Proposições Legislativas

---

## Descrição Geral

O **Nome do Projeto** é um sistema web desenvolvido para monitorar, analisar e facilitar o acesso a proposições legislativas no Brasil. A plataforma permite que usuários busquem leis, acompanhem mudanças e entendam o impacto de decisões legislativas de forma clara e acessível.

---

## 📸 Protótipo
Acesse o protótipo interativo no Figma:
(https://embed.figma.com/design/9Gdfmyo1J2oWtnAmUYd1Vl/Prototipo-Site-MDS?node-id=0-1&t=diM94hTSvFm83IMz-1&embed-host=notion&footer=false&theme=system)

## Integrantes da Equipe
Squad-08 MDS 2026/1 – FGA/UnB
<table>
  <tr>
    <td align="center">
      <img src="assets/images/team/caio-bechepeche.jpg" width="100px;" alt="Caio Bechepeche Mota"/><br />
      <sub><b>NCaio Bechepeche Mota</b></sub><br />
      <a href="https://github.com/CaioMota16">GitHub</a>
    </td>
    <td align="center">
      <img src="assets/images/team/renan-curione.jpg" width="auto;" height="100px;" alt="Renan Curione de Castro"/><br />
      <sub><b>Renan Curione de Castro</b></sub><br />
      <a href="https://github.com/thatsrenan">GitHub</a>
    </td>
    <td align="center">
      <img src="LINK_IMAGEM" width="auto;" height="100px;" alt=" Ítalo Lacerda Martins"/><br />
      <sub><b>Italo Lacerda Martins</b></sub><br />
      <a href="https://github.com/italo-lm">GitHub</a>
    </td>
    <td align="center">
      <img src="LINK_IMAGEM" width="auto;" height="100px;" alt="Luís Henrique Luna de Arruda"/><br />
      <sub><b>Luís Henrique Luna de Arruda</b></sub><br />
      <a href="https://github.com/Donnk61">GitHub</a>
    </td>
    <td align="center">
      <img src="LINK_IMAGEM" width="auto;" height="100px;" alt="Arthur Palhares Ferreira Silva"/><br />
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

Este sistema surge como uma solução para:

- Centralizar dados legislativos  
- Organizar e classificar informações automaticamente  
- Tornar o acompanhamento mais acessível e eficiente  

---

## Tecnologias Utilizadas

- **Front-end:** HTML, CSS, JavaScript , Next
- **Back-end:** Python (Flask) 
- **Consumo de API:** Fetch API  
- **Banco de Dados:** PostgreSQL  
- **Prototipação:** Figma  

---

## Como Executar o Projeto

### Pré-requisitos

Certifique-se de ter instalado:

* Node.js (versão 18 ou superior)
* npm
* PostgreSQL
* Git

---

### 1. Clonar o repositório

```bash
git clone https://github.com/unb-mds/2026-1-Squad08.git
cd nome-do-projeto
```

---

### 2. Criar um ambiente virtual

```bash
python -m venv venv
```

---

### 3. Ativar o ambiente
Windows:
```bash
venv\Scripts\activate
```
Linux/Mac:
``` bash
source venv/bin/activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar o banco de dados (PostgreSQL)

Crie o banco:

```sql
CREATE DATABASE guardioes_da_lei;
```

---

### 6. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz como no exemplo:

```env
PORT=3000

DB_HOST=localhost
DB_PORT=5432
DB_NAME=guardioes_da_lei
DB_USER=postgres
DB_PASSWORD=sua_senha
```

---

### 7. Executar o projeto

```bash
flask run
```

```bash
python app.py
```

---

### 8. Acessar no navegador

```text
http://localhost:3000
```

---

### Observações

Observações
Certifique-se de que o PostgreSQL está em execução
Caso existam migrations:

```bash
flask db upgrade
```
---
## Contribuindo
1. Fork o projeto
2. Crie uma branch para sua feature (<code>git checkout -b feature/nova-feature</code>)
3. Commit suas mudancas (<code>git commit -m 'Adiciona nova feature'</code>)
4. Push para a branch (<code>git push origin feature/nova-feature</code>)
5. Abra um Pull Request
---

## Licenca

---

## Equipe
Desenvolvido como parte do projeto de Metodos de Desenvolvimento de Software (MDS) da Universidade de Brasilia (UnB).