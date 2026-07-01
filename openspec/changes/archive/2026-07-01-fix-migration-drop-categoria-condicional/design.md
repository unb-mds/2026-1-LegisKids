## Context

A cadeia Alembic é: `babbb73a5d52` (schema inicial, sem coluna `categoria`) → `ca57241159f9` → `f3a1b2c4d5e6` → `ded4438e4a2c`. Essa última migration foi escrita assumindo um banco que já tinha passado por um schema antigo com coluna `categoria` legada (presente no Neon de produção antes da limpeza), mas nunca declara essa coluna na migration inicial do repositório. Resultado: `flask db upgrade` do zero falha nessa etapa.

O banco Neon de referência já está no estado final desejado (sem `categoria`, com os índices e a constraint de `favoritos` já aplicados). Não se pode alterá-lo nem recriá-lo — a correção é só no script de migration.

## Goals / Non-Goals

**Goals:**
- `flask db upgrade` do zero deve completar sem erro e chegar ao mesmo schema que o Neon tem hoje.
- Rodar a migration corrigida contra o Neon (que não tem `categoria`) deve ser um no-op para o `drop_column` — sem tentar remover algo inexistente.
- Preservar 100% do restante da migration (índices, coluna `total_descartados`, constraint de `favoritos`).

**Non-Goals:**
- Não reescrever ou squashar o histórico de migrations.
- Não alterar o schema do Neon.
- Não adicionar lógica condicional a outras migrations que não têm esse problema.

## Decisions

- **Verificação via `sqlalchemy.inspect(op.get_bind())`**: dentro de `upgrade()`, usar `Inspector.get_columns('proposicoes')` (ou `has_column`, dependendo da versão do SQLAlchemy disponível) para checar se `categoria` existe antes de chamar `batch_op.drop_column('categoria')`. Alternativa descartada: capturar a exceção `ProgrammingError` do driver com try/except — mais frágil, depende do backend de banco e mascara outros erros reais na mesma transação.
- **Escopo do `batch_alter_table`**: o `drop_column` fica fora do bloco `with op.batch_alter_table(...)` apenas se necessário para condicionar; caso contrário, mantém-se dentro do mesmo bloco, com o `if` envolvendo só a chamada de drop. Os demais `create_index` do mesmo bloco continuam incondicionais (já usam `if_not_exists=True` quando aplicável).
- **`downgrade()` não muda**: o downgrade já recria a coluna `categoria` (linha 58) independentemente de ela ter sido removida ou não no upgrade — isso é seguro pois `add_column` em downgrade assume que a coluna não existe (é a direção inversa de um upgrade bem-sucedido).

## Risks / Trade-offs

- [Risco] Se o Inspector não refletir DDL pendente na mesma transação em algum backend → Mitigação: Postgres com Alembic usa a mesma conexão/transação da migration, e `Inspector.get_columns` consulta o catálogo atual (`information_schema`), refletindo o estado real antes do `drop_column` ser executado.
- [Risco] Duplicar essa lógica condicional vira padrão ad-hoc espalhado pelas migrations → Mitigação: fora de escopo desta mudança; não há outras migrations com o mesmo problema hoje.

## Migration Plan

1. Editar `migrations/versions/ded4438e4a2c_auditoria_backend_total_descartados_e_.py` para condicionar o `drop_column('categoria')`.
2. Validar localmente: `flask db upgrade` em banco Postgres vazio até a `head` sem erros.
3. Validar que rodar a mesma migration contra uma cópia/branch do Neon (que já não tem a coluna) não altera nada além do que já é esperado (índices/constraint, se ainda não aplicados).

Rollback: reverter o arquivo da migration para o estado anterior (git revert do commit), já que não há mudança de estado em bancos existentes.

## Open Questions

Nenhuma.
