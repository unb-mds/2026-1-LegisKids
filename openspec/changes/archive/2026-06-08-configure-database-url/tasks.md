## 1. Configuração de Ambiente

- [x] 1.1 Verificar que `.env` está no `.gitignore` (já existe, confirmar)
- [x] 1.2 Atualizar `.env.example` com `DATABASE_URL` para Docker local e Neon (substituir as 5 vars separadas)
- [x] 1.3 Criar `.env` local com `DATABASE_URL` apontando para o banco Docker local

## 2. Atualização do app.py

- [x] 2.1 Remover a construção manual da URI com `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`
- [x] 2.2 Adicionar leitura de `DATABASE_URL` via `os.getenv("DATABASE_URL")`
- [x] 2.3 Adicionar validação: levantar `RuntimeError` se `DATABASE_URL` for `None` ou vazia
- [x] 2.4 Atribuir `DATABASE_URL` a `app.config["SQLALCHEMY_DATABASE_URI"]`
- [x] 2.5 Verificar que a aplicação sobe corretamente com banco local Docker

## 3. Aplicação no Banco Neon

- [x] 3.1 Obter a connection string real do banco Neon no painel Neon
- [x] 3.2 Substituir temporariamente `DATABASE_URL` no `.env` local pela connection string do Neon
- [x] 3.3 Executar `flask db upgrade` e confirmar que as tabelas foram criadas no Neon
- [x] 3.4 Verificar idempotência do `scripts/seed.py` (não gera duplicatas se rodado mais de uma vez)
- [x] 3.5 Executar `python scripts/seed.py` e confirmar dados iniciais no painel do Neon
- [x] 3.6 Restaurar `DATABASE_URL` no `.env` local para o banco Docker local

## 4. Documentação

- [x] 4.1 Adicionar seção "Configuração do banco de dados" no `README.md` com exemplos de `.env` para Docker local e Neon
- [x] 4.2 Incluir instruções de `flask db upgrade` e `python scripts/seed.py` na seção

## 5. GitHub Secret

- [ ] 5.1 Adicionar o GitHub Secret `DATABASE_URL` com a connection string real do Neon no repositório (Settings → Secrets → Actions)
- [x] 5.2 Confirmar que a connection string real não aparece em nenhum arquivo versionado (`git log --all -S "neon.tech"`)

## 6. Validação Final

- [x] 6.1 Confirmar que a aplicação sobe com banco Docker local (após restaurar `.env` local)
- [ ] 6.2 Confirmar que pelo menos um outro membro do time consegue conectar ao banco Neon com a connection string compartilhada de forma segura
- [x] 6.3 Confirmar que o painel do Neon mostra as tabelas criadas e os dados iniciais inseridos
