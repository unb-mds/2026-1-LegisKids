## Context

O dashboard de produtividade é gerado por `scripts/generate_performance_report.py` como HTML estático. A versão atual passou a combinar trechos da página antiga com trechos da página nova e contém JavaScript inválido em runtime, interrompendo a renderização depois do resumo por aluno.

## Goals / Non-Goals

**Goals:**
- Garantir que o HTML gerado seja uma página única, coerente e sem trechos legados misturados.
- Preservar o dashboard interativo com filtros, KPIs, gráficos e tabelas.
- Validar o JavaScript embutido extraído do HTML gerado.
- Manter funcionamento via `file://` com dados embutidos.

**Non-Goals:**
- Alterar o conjunto de métricas coletadas.
- Criar novo framework frontend ou build step.
- Mudar o workflow de coleta além do necessário para regenerar os artefatos.

## Decisions

- Substituir `string.Template` por substituição explícita de placeholders sentinela (`__REPOSITORY__`, `__GENERATED_AT__`, `__DATA_JSON__`) para evitar conflito com template literals JavaScript como `${row.value}`.
- Regenerar `docs/performance/index.html` exclusivamente a partir do template corrigido, eliminando qualquer HTML legado.
- Manter o JSON embutido em `<script type="application/json">` para continuar funcionando sem servidor.
- Validar o script extraído do HTML com `node --check`, além de compilar o Python.

## Risks / Trade-offs

- **Erro JavaScript futuro não detectado por abertura manual** -> Mitigação: extrair o `<script>` do HTML e validar sintaxe com Node durante a correção.
- **Dados reais de issues/PRs dependem do GitHub Actions** -> Mitigação: validar localmente o schema e a renderização com os dados disponíveis; a coleta remota continua no workflow.
- **HTML grande por dados embutidos** -> Mitigação: manter a abordagem para garantir `file://`; otimização de tamanho fica fora desta correção.
