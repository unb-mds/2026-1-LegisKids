# Implementação dos Models SQLAlchemy — LegisKids

> Esta documentação cobre a issue:
>
> * Issue #174 — Implementação dos Models SQLAlchemy com relacionamentos, validações e métodos auxiliares

---

# O que foi feito

## Issue #174 — Models SQLAlchemy

| Arquivo                 | O que faz                                                                                                         |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `src/backend/models.py` | Implementa todos os models SQLAlchemy com relacionamentos, serialização (`to_dict`) e representação (`__repr__`). |
| `test_models.py`        | Script de teste para validar criação de registros, relacionamentos e serialização JSON.                           |

---

# Models criados

| Model               | Tabela                | Finalidade                                                    |
| ------------------- | --------------------- | ------------------------------------------------------------- |
| `Partido`           | `partidos`            | Representa partidos políticos associados às proposições.      |
| `Proposicao`        | `proposicoes`         | Armazena proposições legislativas coletadas da API da Câmara. |
| `Tramitacao`        | `tramitacoes`         | Histórico de tramitação das proposições.                      |
| `Usuario`           | `usuarios`            | Usuários autenticados via Google OAuth.                       |
| `Favorito`          | `favoritos`           | Relação entre usuários e proposições favoritados.             |
| `HistoricoConsulta` | `historico_consultas` | Histórico de pesquisas realizadas pelos usuários.             |
| `RequisicaoApi`     | `requisicoes_api`     | Registro e auditoria das coletas realizadas na API da Câmara. |

---

# Relacionamentos

```text
partidos ──────────────── proposicoes          (1:N)
proposicoes ──────────── tramitacoes           (1:N)
proposicoes ──────────── favoritos             (1:N)
usuarios ─────────────── favoritos             (1:N)
usuarios ─────────────── historico_consultas   (1:N)
```

## Regras de negócio

### Partido → Proposição

* Um partido pode possuir várias proposições.
* Cada proposição pertence a um único partido.

### Proposição → Tramitação

* Uma proposição pode possuir várias tramitações.
* Cada tramitação pertence a uma única proposição.

### Usuário → Favorito

* Um usuário pode favoritar várias proposições.
* Uma proposição pode ser favoritada por vários usuários.

### Usuário → Histórico de Consulta

* Um usuário pode possuir diversas consultas registradas.
* Cada consulta pertence a um único usuário.

---

# Recursos implementados em todos os models

Todos os models possuem:

* `db.relationship()` com `back_populates`
* Navegação bidirecional entre entidades
* `to_dict()` para serialização JSON
* `__repr__()` para depuração
* Chaves estrangeiras (`ForeignKey`)
* Regras de integridade referencial

Nos relacionamentos dependentes foram utilizados:

```python
cascade="all, delete-orphan"
```

Para garantir que registros filhos sejam removidos automaticamente quando o registro pai for excluído.

Também foram utilizadas regras:

```python
ondelete="CASCADE"
```

e

```python
ondelete="SET NULL"
```

conforme a necessidade de cada relacionamento.

---

# Estrutura dos Models

## Partido

| Campo | Tipo    |
| ----- | ------- |
| id    | Integer |
| sigla | String  |
| nome  | String  |

Relacionamentos:

```python
proposicoes
```

---

## Proposicao

| Campo              | Tipo     |
| ------------------ | -------- |
| id                 | Integer  |
| sigla_tipo         | String   |
| numero             | Integer  |
| ano                | Integer  |
| ementa             | Text     |
| data_apresentacao  | Date     |
| descricao_situacao | String   |
| sigla_partido      | String   |
| categoria          | String   |
| data_coleta        | DateTime |
| partido_id         | Integer  |

Relacionamentos:

```python
partido
tramitacoes
favoritos
```

---

## Tramitacao

| Campo           | Tipo    |
| --------------- | ------- |
| id              | Integer |
| proposicao_id   | Integer |
| data_tramitacao | Date    |
| descricao       | Text    |

Relacionamentos:

```python
proposicao
```

---

## Usuario

| Campo     | Tipo    |
| --------- | ------- |
| id        | Integer |
| nome      | String  |
| email     | String  |
| google_id | String  |
| foto_url  | String  |

Relacionamentos:

```python
favoritos
historico_consultas
```

---

## Favorito

| Campo         | Tipo     |
| ------------- | -------- |
| id            | Integer  |
| usuario_id    | Integer  |
| proposicao_id | Integer  |
| data_favorito | DateTime |

Relacionamentos:

```python
usuario
proposicao
```

---

## HistoricoConsulta

| Campo         | Tipo     |
| ------------- | -------- |
| id            | Integer  |
| usuario_id    | Integer  |
| termo_busca   | String   |
| data_consulta | DateTime |

Relacionamentos:

```python
usuario
```

---

## RequisicaoApi

| Campo           | Tipo     |
| --------------- | -------- |
| id              | Integer  |
| endpoint        | String   |
| status_code     | Integer  |
| data_requisicao | DateTime |
| tempo_resposta  | Float    |

---

# Serialização JSON

Todos os models implementam:

```python
to_dict()
```

que converte os objetos para estruturas compatíveis com JSON.

Exemplo:

```python
prop.to_dict()
```

Retorno:

```json
{
  "id": 3,
  "sigla_tipo": "PEC",
  "numero": 8888,
  "ano": 2025,
  "ementa": "Texto da ementa",
  "data_apresentacao": "2025-01-01",
  "descricao_situacao": "Em tramitação",
  "sigla_partido": "MDB",
  "categoria": null,
  "data_coleta": "2026-06-10T00:18:23.309107",
  "partido": {
    "id": 4,
    "sigla": "MDB",
    "nome": "Movimento Democrático Brasileiro"
  }
}
```

Datas e horários são convertidos utilizando:

```python
.isoformat()
```

garantindo compatibilidade com clientes REST e aplicações frontend.

---

# Como utilizar os models

## Inserindo dados

```python
from src.backend.app import app
from src.backend.database import db
from src.backend.models import Partido, Proposicao
from datetime import date

with app.app_context():

    partido = Partido(
        sigla='PT',
        nome='Partido dos Trabalhadores'
    )

    db.session.add(partido)
    db.session.flush()

    proposicao = Proposicao(
        sigla_tipo='PL',
        numero=1234,
        ano=2024,
        ementa='Dispõe sobre saúde pública',
        data_apresentacao=date(2024, 3, 1),
        descricao_situacao='Em tramitação',
        sigla_partido='PT',
        partido=partido
    )

    db.session.add(proposicao)
    db.session.commit()
```

---

## Consultando dados

```python
from src.backend.models import Proposicao

proposicoes = Proposicao.query.all()
```

Filtrar:

```python
props = Proposicao.query.filter_by(
    categoria='cyberbullying'
).all()
```

Buscar por ID:

```python
prop = db.session.get(Proposicao, 1)
```

Serializar:

```python
dados = prop.to_dict()
```

---

# Navegando pelos relacionamentos

## Da proposição para o partido

```python
prop = Proposicao.query.first()

print(prop.partido.nome)
```

---

## Do partido para suas proposições

```python
partido = Partido.query.first()

for prop in partido.proposicoes:
    print(prop.numero)
```

---

## Favoritos de um usuário

```python
usuario = Usuario.query.first()

for favorito in usuario.favoritos:
    print(favorito.proposicao.ementa)
```

---

# Exemplo de Repository

```python
from src.backend.database import db
from src.backend.models import Proposicao

def buscar_todas():
    return Proposicao.query.all()

def buscar_por_id(id):
    return db.session.get(Proposicao, id)

def inserir(proposicao):
    db.session.add(proposicao)
    db.session.commit()
    return proposicao
```

---

# Arquitetura sugerida

```text
Routes / Controllers
          ↓
       Services
          ↓
      Repositories
          ↓
        Models
          ↓
      PostgreSQL
```

Responsabilidades:

* Routes: recebem requisições HTTP.
* Services: implementam regras de negócio.
* Repositories: encapsulam acesso ao banco.
* Models: representam entidades persistidas.
* PostgreSQL: armazenamento dos dados.

---

# Testando os models

Execute:

```bash
python test_models.py
```

Saída esperada:

```text
=== REPR ===
<Partido MDB>
<Proposicao PEC 8888/2025>
<Usuario dict@exemplo.com>
<Favorito user=3 prop=3>

=== TO_DICT ===
Partido: {...}
Proposicao: {...}
Usuario: {...}
Favorito: {...}

OK Todos os to_dict() funcionando!
```

---

# Fluxo para alterações futuras

## Adicionar um novo campo

1. Editar o model em `models.py`
2. Gerar migration

```bash
flask db migrate -m "descricao da mudanca"
```

3. Revisar o arquivo gerado
4. Aplicar no banco

```bash
flask db upgrade
```

Importante:

> Sempre commitar os arquivos de migration junto com a alteração do model.

---

## Atualizar banco após dar pull

```bash
flask db upgrade
```

---

# Comandos úteis

| Situação                | Comando                           |
| ----------------------- | --------------------------------- |
| Testar models           | `python test_models.py`           |
| Criar migration         | `flask db migrate -m "descricao"` |
| Aplicar migration       | `flask db upgrade`                |
| Reverter migration      | `flask db downgrade`              |
| Histórico de migrations | `flask db history`                |

---

# Problemas comuns

## UniqueViolation

O banco já possui registros criados pelo teste.

Solução:

* utilizar dados diferentes;
* remover registros de teste;
* limpar as tabelas antes da execução.

---

## IntegrityError por sequência desincronizada

Executar:

```sql
SELECT setval(
    'partidos_id_seq',
    (SELECT MAX(id) FROM partidos)
);
```

---

## python-dotenv could not parse statement

O arquivo `.env` foi salvo com encoding incorreto.

Recrie o arquivo:

```powershell
[System.IO.File]::WriteAllText(
"$PWD\.env",
"DATABASE_URL=...",
[System.Text.UTF8Encoding]::new($false)
)
```

---

## RuntimeError: DATABASE_URL não configurada

Verifique:

* existência do arquivo `.env`;
* chamada de `load_dotenv()`;
* caminho utilizado para carregar o `.env`;
* variável `DATABASE_URL` definida corretamente.
