## 1. Serializer

- [x] 1.1 Em `src/backend/controllers/proposicoes_controller.py`, na função `_serializar_proposicao`, substituir `d["subtema"] = cats[0]["nome"] if cats else None` por `d["subtemas"] = [c["nome"] for c in cats]`

## 2. Testes

- [x] 2.1 Adicionar/atualizar teste cobrindo `GET /api/proposicoes` para uma proposição com múltiplas categorias, verificando que `items[].subtemas` contém todos os nomes (não só o primeiro)
- [x] 2.2 Adicionar/atualizar teste cobrindo `GET /api/proposicoes/<id>` para uma proposição com múltiplas categorias, verificando que `proposicao.subtemas` contém todos os nomes
- [x] 2.3 Adicionar/atualizar teste cobrindo o caso de proposição sem categorias, verificando que `subtemas` é `[]` (não `null`)
- [x] 2.4 Rodar a suíte de testes do backend e confirmar que nenhum teste existente ainda referencia o campo `subtema` (singular)

## 3. Verificação final

- [x] 3.1 Confirmar via `git diff` que apenas arquivos em `src/backend/` (e `tests/`, se aplicável) foram alterados — nenhum arquivo de frontend tocado
- [ ] 3.2 Atualizar a descrição do PR `fix/backend` avisando que o merge deve ser coordenado com `fix/frontend` (campo `subtema` → `subtemas`)
