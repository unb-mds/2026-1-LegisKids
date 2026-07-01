## Context

`Proposicao.to_dict()` já serializa `categorias` como lista completa (via relação `proposicao_categorias`). O bug está inteiramente em `_serializar_proposicao()`, que reduz essa lista a um único nome (`cats[0]["nome"]`) armazenado no campo `subtema`. Isso afeta as duas rotas que reutilizam essa função: `GET /api/proposicoes` (listagem) e `GET /api/proposicoes/<id>` (detalhe).

## Goals / Non-Goals

**Goals:**
- Expor todas as categorias de uma proposição na resposta HTTP, não apenas a primeira.
- Manter a mudança isolada em `src/backend/controllers/proposicoes_controller.py` — sem alterar models, repository ou schema.

**Non-Goals:**
- Não introduzir conceito de "subtema primário vs. secundário" (isso é escopo de US06, fora desta mudança).
- Não manter `subtema` como alias de compatibilidade — a troca é direta, coordenada com o PR de frontend.
- Não alterar o filtro `?subtema=` de `GET /api/proposicoes` (continua filtrando por nome de categoria via `EXISTS`, sem mudança de contrato de request).

## Decisions

- **Renomear `subtema` → `subtemas` (array) em vez de manter ambos os campos**: o CLAUDE.md e o schema já tratam a relação proposição↔categoria como muitos-para-muitos; manter um campo singular ao lado do array seria dado redundante e incorreto (qual seria "a" categoria principal quando não existe conceito de primária?). Decisão: campo único `subtemas: string[]`, ordenado pela ordem retornada por `prop.categorias` (ordem de inserção).
- **Reaproveitar `d["categorias"]` já serializado**: `_serializar_proposicao` já tem `cats = d.get("categorias", [])`; basta mapear `[c["nome"] for c in cats]` em vez de pegar `cats[0]`. Nenhuma nova query ao banco é necessária.

## Risks / Trade-offs

- [Breaking change quebra o frontend em produção se mergeado sozinho] → Mitigação: proposal.md documenta explicitamente que `fix/backend` e `fix/frontend` devem ser mergeados juntos; PR description deve citar essa dependência.
- [Specs `api-proposicoes-list` e `api-proposicoes-detail` ficam desatualizadas se não revisadas] → Mitigação: specs desta mudança já incluem os deltas MODIFIED necessários.
