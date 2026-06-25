## Context

O banco do LegisKids possui 7 tabelas definidas nos models SQLAlchemy (`src/backend/models.py`) e versionadas via Flask-Migrate. A documentação existente (`guia_integrantes.md`) cobre configuração de ambiente mas não descreve o schema de forma estruturada — sem colunas, tipos, constraints nem ERD. A fonte de verdade do schema é o `models.py`.

## Goals / Non-Goals

**Goals:**
- Produzir um ERD visual (`.png`) e seu código-fonte editável (`.dbml`) a partir do schema real
- Produzir `docs/db/schema.md` com tabelas, colunas, tipos, nulidade, constraints, relacionamentos e decisões de design
- Integrar a documentação ao MkDocs e ao README

**Non-Goals:**
- Alterar qualquer tabela, model ou migration
- Criar novo banco de dados ou ambiente
- Automatizar geração futura do ERD (manutenção manual via `.dbml`)

## Decisions

**1. Fonte de verdade: `models.py`, não o banco em si**
O `models.py` é o artefato mais próximo da intenção de design — contém comentários, nomes semânticos e está no git. O banco físico pode ter defasagem se migrations não foram rodadas. A documentação reflete o que está nos models.

**2. Formato do ERD: `.dbml` + exportação `.png`**
O DBML (Database Markup Language) é texto versionável, editável por qualquer membro sem ferramenta especializada, e é o formato nativo do `dbdiagram.io` — ferramenta gratuita que exporta `.png` de qualidade. Alternativas como PlantUML ou Mermaid são viáveis mas menos visuais para ERDs relacionais.

**3. Localização: `docs/db/`**
Separa documentação de banco da documentação de estudos genéricos (`docs/estudos/banco_de_dados/`). O diretório `docs/db/` fica alinhado com a convenção usada em outros projetos de engenharia.

**4. ERD gerado manualmente (não automatizado)**
A geração automática via `sqlacodegen` ou `eralchemy` exigiria dependência extra e acesso ao banco em tempo de CI. Como o schema é estável para a Release 1, a criação manual do `.dbml` é suficiente e mais legível.

## Risks / Trade-offs

- **ERD desatualizado após migrations futuras** → Mitigação: o `.dbml` é versionado no git; toda PR que alterar models deve atualizar o `.dbml` e re-exportar o `.png`. Isso é documentado no `schema.md`.
- **Divergência entre `models.py` e banco físico** → Mitigação: a documentação declara explicitamente que reflete o `models.py` e instrui o leitor a rodar `flask db upgrade` para sincronizar o banco.
- **Ferramenta de ERD externa (dbdiagram.io)** → Mitigação: o `.dbml` é suficiente para recriar o diagrama em qualquer ferramenta compatível; o `.png` gerado é estático e não depende da ferramenta após a exportação.

## Migration Plan

1. Criar `docs/db/erd.dbml` com o schema completo em DBML
2. Exportar `docs/db/erd.png` via `dbdiagram.io`
3. Criar `docs/db/schema.md` referenciando o ERD e descrevendo cada tabela
4. Atualizar `README.md` com link para `docs/db/schema.md`
5. Atualizar `mkdocs.yml` com entrada para `docs/db/schema.md`

Rollback: não há impacto em código — todos os arquivos são documentação. Reverter é apagar os arquivos criados.
