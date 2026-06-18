---
name: python-style
description: Use this skill for any general Python code in the LegisKids backend that isn't specifically about Flask routing or SQLAlchemy models — utility functions, data processing/parsing of legislative data, type hints, error handling patterns, project-wide style, virtual environments, and requirements.txt management. Triggers on writing or refactoring .py files, discussing PEP 8, type hints, or "boas práticas Python". For Flask-specific routing use flask-backend; for ORM/queries use sqlalchemy-orm.
---

# Python — Padrões do LegisKids

## Estilo e convenções

- Siga PEP 8: 4 espaços, linhas até ~99 colunas, `snake_case` para funções/variáveis, `PascalCase` para classes.
- Use type hints em toda função pública, especialmente nas que cruzam camadas (`service -> route`, `service -> model`):

```python
def listar_proposicoes(pagina: int = 1, tema: str | None = None) -> dict[str, object]:
    ...
```

- Docstrings curtas em português (consistente com o domínio do projeto: nomes de campos legislativos, ementas, etc.), formato Google-style:

```python
def calcular_impacto(proposicao_id: int) -> float:
    """Calcula uma pontuação de impacto estimado da proposição.

    Args:
        proposicao_id: identificador da proposição no banco.

    Returns:
        Pontuação entre 0 e 1.
    """
```

## Organização de dependências

- `requirements.txt` versionado com pins exatos (`Flask==3.0.3`) para reprodutibilidade do ambiente da equipe e do CI.
- Separe dependências de desenvolvimento (`pytest`, `black`, `ruff`) em `requirements-dev.txt` ou usar `pip-tools`/`poetry` se o time migrar para isso.
- Sempre trabalhar dentro de um virtualenv (`python -m venv venv`), nunca instalar pacotes globalmente — isso é coerente com o próprio README do projeto.

## Tratamento de erros e exceções

Evite `except Exception: pass` silencioso. Prefira exceções específicas e logue o contexto:

```python
import logging

logger = logging.getLogger(__name__)

try:
    resposta = requests.get(url, timeout=10)
    resposta.raise_for_status()
except requests.Timeout:
    logger.warning("Timeout ao consultar API da Câmara: %s", url)
    raise
except requests.HTTPError as e:
    logger.error("Erro HTTP %s ao consultar %s", e.response.status_code, url)
    raise
```

## Parsing e normalização de dados legislativos

Dados de proposições costumam vir de fontes externas (API da Câmara dos Deputados, scraping, etc.) com formatos inconsistentes. Centralize normalização em funções puras e testáveis:

```python
def normalizar_tema(tema_bruto: str) -> str:
    """Normaliza string de tema vinda da fonte externa para o vocabulário interno."""
    return tema_bruto.strip().lower().replace("  ", " ")
```

Nunca faça parsing de data/hora manualmente com slicing de string — use `datetime.fromisoformat` ou `dateutil.parser`.

## Funções puras vs. efeitos colaterais

Separe claramente:
- Funções de **transformação** (input -> output, sem I/O) — fáceis de testar unitariamente.
- Funções de **orquestração** (chamam banco, API externa, Gemini) — testadas com mocks/integração.

Isso facilita testar a lógica de negócio sem precisar de banco de dados ou rede.

## Logging

Use o módulo `logging` configurado uma vez na app factory, nunca `print()` em código de produção:

```python
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
```

## Testes

- `pytest` como padrão; nomeie arquivos `test_*.py` e funções `test_*`.
- Use fixtures (`conftest.py`) para banco de teste, app Flask de teste, e mocks de serviços externos (Gemini, API da Câmara).
- Cubra principalmente: parsing/normalização de dados, regras de negócio, e os contratos das rotas (status code + shape do JSON).

## Checklist rápido

1. Type hints nas assinaturas públicas.
2. Sem `print()`; usar `logging`.
3. Exceções específicas, nunca `except:` genérico sem re-raise ou log.
4. Dependências pinadas no `requirements.txt`.
5. Funções de parsing/normalização isoladas e testadas.
