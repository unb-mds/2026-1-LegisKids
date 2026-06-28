# Design — auditoria-backend-pre-develop

## Arquivos afetados

| Arquivo | Ação |
|---|---|
| `src/backend/models.py` | Adicionar coluna `total_descartados` em `SyncExecution` |
| `src/backend/services/camara_service.py` | Corrigir detecção de falha Gemini e passar `total_descartados` |
| `src/backend/migrations/testa_tabelas.py` | Remover |
| `migrations/versions/<nova>.py` | Migration: coluna `total_descartados` + índice `classificacao_status` |

---

## Fix 1 — `cota_gemini_esgotada` (camara_service.py)

O problema é que `_classificar_lote()` nunca lança — ela captura internamente e retorna `None` por DTO. O bloco `except Exception` em `run_sync` que setaria a flag nunca é alcançado.

**Solução:** logo após `pares = self._classificar_lote(lote)`, checar se todos os resultados foram `None`:

```python
pares = self._classificar_lote(lote)
dtos_com_resultado.extend(pares)

# Detecta falha total do Gemini neste lote (todos retornaram None)
if all(categorias is None for _, categorias in pares):
    cota_gemini_esgotada = True
```

Remover o bloco `except Exception` externo que envolvia `self._classificar_lote(lote)` em `run_sync`, pois nunca é alcançado e obscurece o fluxo.

**Resultado:** quando o Gemini falha num lote, os próximos lotes e páginas pulam a chamada (já era o comportamento pretendido), e o status final registrado é `concluido_parcial`.

---

## Fix 2 — `total_descartados` (model + service + migration)

### `SyncExecution` em `models.py`

Adicionar coluna após `total_erros`:
```python
total_descartados = db.Column(db.Integer, nullable=False, default=0)
```

Atualizar `to_dict()` para incluir o campo.

### `run_sync()` em `camara_service.py`

Incluir `total_descartados` na chamada a `atualizar_sync_execution`:
```python
repo.atualizar_sync_execution(
    execucao.id,
    ...
    total_erros=total_erros,
    total_descartados=total_descartados,   # ← adicionar
    mensagem_erro=mensagem_erro,
)
```

### Migration

```python
def upgrade():
    # Coluna total_descartados
    with op.batch_alter_table('sync_executions', schema=None) as batch_op:
        batch_op.add_column(sa.Column(
            'total_descartados', sa.Integer(), nullable=False, server_default='0'
        ))

    # Índice em classificacao_status
    with op.batch_alter_table('proposicoes', schema=None) as batch_op:
        batch_op.create_index(
            'idx_proposicoes_classificacao_status', ['classificacao_status'], unique=False
        )
```

---

## Fix 3 — Índice em `classificacao_status` (migration + model)

### Model (`models.py`)

Adicionar o índice à `__table_args__` de `Proposicao`:
```python
db.Index('idx_proposicoes_classificacao_status', 'classificacao_status'),
```

O índice em si é criado pela migration.

---

## Fix 4 — Remover `testa_tabelas.py`

Deletar `src/backend/migrations/testa_tabelas.py` sem substituição.

---

## Fluxo de `run_sync()` após as correções

```
run_sync()
│
├── _retentar_pendentes()
│
└── loop de páginas
    ├── _buscar_proposicoes_api()
    ├── early-stop se todos IDs conhecidos
    ├── _filtrar_por_palavras_chave()
    ├── _validar_proposicao()
    ├── skip de IDs conhecidos
    └── para cada lote de dtos_validos:
        ├── se cota_gemini_esgotada → marca como pendente, continua
        ├── _classificar_lote()  ← nunca lança, retorna (dto, None) se Gemini falhou
        ├── [NOVO] se todos None → cota_gemini_esgotada = True
        └── filtra irrelevantes, persiste, vincula categorias
│
└── atualizar_sync_execution(... total_descartados=total_descartados ...)  ← persiste agora
```

---

## Nenhuma mudança em

- Prompt do Gemini / lógica de classificação
- Lógica de paginação / early-stop / skip
- `_retentar_pendentes`
- Scheduler
- Relacionamentos N:N
- Testes existentes (devem continuar passando sem alteração)
