# Design — limpeza-backend

## Arquivos afetados

| Arquivo | Ação |
|---|---|
| `src/backend/main.py` | Remover |
| `src/backend/services/camara_api.py` | Remover |
| `src/backend/models.py` | Editar — corrigir `datetime.utcnow` |
| `src/backend/repository/camara_repository.py` | Editar — remover commit interno de `vincular_categoria` |
| `tests/test_camara_service.py` | Verificar — não importa os arquivos removidos |
| `tests/test_camara_repository.py` | Verificar — não importa os arquivos removidos |

---

## 1. Remoção de `main.py`

**Problema:** O arquivo executa código no nível do módulo (`int(input(...))`) — importá-lo congela o processo. Implementa uma CLI interativa que foi substituída pelo comando Flask `sync-camara` + scheduler automático.

**Ação:** `git rm src/backend/main.py`

**Verificação:** Nenhum arquivo no projeto importa `main.py` (confirmar com grep antes de remover).

---

## 2. Remoção de `camara_api.py`

**Problema:** Define três funções que são subconjuntos do que `camara_service.py` já faz:

| `camara_api.py` | Equivalente em `camara_service.py` |
|---|---|
| `URL_BASE` | `URL_BASE` (mesma constante) |
| `listar_proposicoes()` | `_buscar_proposicoes_api()` |
| `filtrar_por_palavras_chave()` | `_filtrar_por_palavras_chave()` |
| `buscarCodTema()` | não usada no pipeline atual |

**Ação:** `git rm src/backend/services/camara_api.py`

**Verificação:** `main.py` (já removido) era o único importador. Confirmar com grep.

---

## 3. Correção de `datetime.utcnow` em `models.py`

**Problema:** `datetime.utcnow` está deprecated desde Python 3.12. Emite `DeprecationWarning` e será removido numa versão futura.

**Padrão correto** (já usado em `SyncExecution`):
```python
default=lambda: datetime.now(timezone.utc)
```

**Modelos afetados:**

```python
# Proposicao
data_coleta = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
# → default=lambda: datetime.now(timezone.utc)

# Usuario
data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
# → default=lambda: datetime.now(timezone.utc)

# Favorito
data_favorito = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
# → default=lambda: datetime.now(timezone.utc)

# HistoricoConsulta
data_consulta = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
# → default=lambda: datetime.now(timezone.utc)

# RequisicaoApi
data_requisicao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
# → default=lambda: datetime.now(timezone.utc)
```

---

## 4. Remoção do commit interno de `vincular_categoria`

**Problema atual:**
```python
def vincular_categoria(proposicao_id: int, categoria_nome: str) -> None:
    ...
    db.session.execute(stmt)
    db.session.commit()  # ← commit por chamada
```

Com múltiplas categorias por proposição e lotes de 50, isso gera dezenas de commits individuais onde um único bastaria.

**Solução:** Remover o `db.session.commit()` de `vincular_categoria`. O commit já é feito pelo chamador (`upsert_proposicoes_lote` e `atualizar_classificacao_status` em `camara_repository.py`).

**Após a mudança**, o fluxo em `run_sync` fica:
1. `upsert_proposicoes_lote(dtos)` → 1 commit para N proposições
2. `vincular_categoria(id, cat)` × M → só `execute`, sem commit
3. `atualizar_classificacao_status(id, status)` → commit final

Para manter corretude em `_retentar_pendentes`, onde `vincular_categoria` é chamada sem `upsert` após, adicionar um `db.session.commit()` explícito após o loop de categorias nessa função.

---

## Verificações pré-remoção

```bash
# Confirmar que nenhum arquivo ativo importa main.py
grep -r "from.*main import\|import main" src/ tests/ --include="*.py"

# Confirmar que nenhum arquivo ativo importa camara_api
grep -r "camara_api" src/ tests/ --include="*.py"
```
