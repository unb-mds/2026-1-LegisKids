## 1. Preparação

- [x] 1.1 Ler `src/backend/models.py` na íntegra para levantar todas as tabelas, colunas, tipos, nulidade e constraints
- [x] 1.2 Verificar os arquivos em `migrations/versions/` para confirmar que o schema dos models está aplicado
- [x] 1.3 Criar o diretório `docs/db/`

## 2. ERD — Código-fonte DBML

- [x] 2.1 Criar `docs/db/erd.dbml` com todas as 7 tabelas do banco (`partidos`, `proposicoes`, `tramitacoes`, `usuarios`, `favoritos`, `historico_consultas`, `requisicoes_api`)
- [x] 2.2 Incluir no DBML: colunas com tipo e nullable, primary keys, unique constraints e foreign keys com `ON DELETE`
- [x] 2.3 Incluir no DBML: relacionamentos com cardinalidade (ref: um-para-muitos)

## 3. ERD — Imagem PNG

- [x] 3.1 Importar `docs/db/erd.dbml` no [dbdiagram.io](https://dbdiagram.io), revisar o diagrama visualmente
- [x] 3.2 Exportar o diagrama como `docs/db/erd.png`

## 4. Documentação textual — schema.md

- [x] 4.1 Criar `docs/db/schema.md` com seção de visão geral do banco e imagem embutida do ERD
- [x] 4.2 Documentar tabela `partidos`: propósito, colunas, PK, unique constraint em `sigla`
- [x] 4.3 Documentar tabela `proposicoes`: propósito, colunas (incluindo `partido_id` nullable e `categoria`), PK, FK, unique constraint composta
- [x] 4.4 Documentar tabela `tramitacoes`: propósito, colunas, PK, FK com `ON DELETE CASCADE`
- [x] 4.5 Documentar tabela `usuarios`: propósito, colunas, PK, unique constraints em `email` e `google_id`
- [x] 4.6 Documentar tabela `favoritos`: propósito, colunas, PK, FKs com `ON DELETE CASCADE`, unique constraint composta
- [x] 4.7 Documentar tabela `historico_consultas`: propósito, colunas, PK, FK com `ON DELETE CASCADE`
- [x] 4.8 Documentar tabela `requisicoes_api`: propósito, colunas, PK, campo `tempo_execucao_ms` nullable
- [x] 4.9 Adicionar seção de relacionamentos com cardinalidades e justificativa de cada relação
- [x] 4.10 Adicionar seção de índices e constraints listando PKs, FKs (com `ON DELETE`), unique constraints e comportamentos relevantes
- [x] 4.11 Adicionar seção de decisões de design explicando: `partido_id` nullable em `proposicoes`, unique composta em `favoritos`, tabela `requisicoes_api` como log de auditoria, `categoria` como campo derivado

## 5. Integração — README e MkDocs

- [x] 5.1 Adicionar no `README.md` referência a `docs/db/schema.md` e ao ERD na seção de banco de dados
- [x] 5.2 Adicionar entrada em `mkdocs.yml` para `docs/db/schema.md` na seção de Banco de Dados

## 6. Validação

- [x] 6.1 Confirmar que todos os campos do `models.py` estão presentes no `schema.md`
- [x] 6.2 Confirmar que o ERD no `erd.png` representa o mesmo schema do `schema.md`
- [x] 6.3 Confirmar que os links no README apontam para os arquivos corretos
- [x] 6.4 Confirmar que a entrada no MkDocs está correta e o arquivo é exibido na navegação
