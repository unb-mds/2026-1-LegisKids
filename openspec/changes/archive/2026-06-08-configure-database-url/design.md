## Context

O `src/backend/app.py` constrói a URI de conexão ao banco montando manualmente 5 variáveis separadas (`DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`). Isso cria dois problemas: (1) cada desenvolvedor precisa configurar 5 variáveis em vez de uma; (2) o padrão não é compatível diretamente com bancos externos como Neon, que exigem parâmetros extras como `sslmode=require`.

O `.gitignore` já protege `.env`. O Flask-Migrate já está configurado. O banco de dados local usa Docker.

## Goals / Non-Goals

**Goals:**
- Migrar `app.py` para usar uma única variável `DATABASE_URL` em `SQLALCHEMY_DATABASE_URI`
- Atualizar `.env.example` para documentar os dois modos de conexão (Docker local, Neon remoto)
- Garantir que `sslmode=require` seja preservado quando presente na URL
- Aplicar as migrations existentes no banco Neon e popular com seed
- Documentar o setup no README
- Configurar o GitHub Secret `DATABASE_URL`

**Non-Goals:**
- Criar ou alterar tabelas/migrations
- Alterar modelo de dados ou lógica de negócio
- Configurar deploy em produção ou CI/CD completo

## Decisions

**Decisão 1: `DATABASE_URL` como única fonte de verdade**

Alternativa considerada: manter as 5 variáveis separadas e adicionar lógica para detectar qual usar.

Escolha: `DATABASE_URL` apenas. Motivo: é o padrão de facto do ecossistema Python/Flask (Heroku, Render, Railway, Neon), reduz configuração de 5 para 1, e SQLAlchemy aceita diretamente. Sem código extra de composição.

**Decisão 2: Validar `DATABASE_URL` na inicialização**

O app deve levantar `RuntimeError` se `DATABASE_URL` não estiver definida, em vez de falhar silenciosamente mais tarde com erro de conexão. Isso torna o erro imediatamente óbvio para o desenvolvedor.

**Decisão 3: Não modificar `sslmode` no código**

O código não deve adicionar nem remover parâmetros da URL. Se a URL contém `?sslmode=require` (Neon), será repassada intacta ao SQLAlchemy, que a suporta. Sem lógica condicional de SSL — o comportamento vem da URL.

**Decisão 4: `.env.example` como documentação, não segredo**

O `.env.example` mostrará apenas exemplos com placeholder (`usuario`, `senha`, `host.neon.tech`). A connection string real do Neon vai apenas no GitHub Secret e no `.env` local de cada desenvolvedor (nunca commitado).

## Risks / Trade-offs

- **Migração causa breaking change local**: qualquer desenvolvedor que não atualizar seu `.env` local vai quebrar ao puxar a mudança. Mitigação: README claro + `.env.example` atualizado indicando o que fazer.
- **Seed idempotente**: rodar `scripts/seed.py` múltiplas vezes pode inserir duplicatas. Mitigação: documentar que seed deve ser rodado apenas uma vez no banco Neon; o script deve ser verificado para conflitos antes da execução.
- **Neon free tier**: armazenamento limitado. Mitigação: sem impacto neste escopo (apenas migrations + seed de dados iniciais mínimos).

## Migration Plan

1. Atualizar `.env.example` com nova estrutura `DATABASE_URL`
2. Atualizar `src/backend/app.py` para usar `DATABASE_URL`
3. Atualizar `.gitignore` se necessário (já contém `.env`)
4. Atualizar `README.md` com seção de configuração do banco
5. Desenvolvedores atualizam `.env` local removendo as 5 vars e adicionando `DATABASE_URL`
6. Com `.env` local apontando para Neon: `flask db upgrade` + `python scripts/seed.py`
7. Adicionar GitHub Secret `DATABASE_URL` no repositório

Rollback: reverter `app.py` para montagem manual das 5 vars e restaurar `.env.example` anterior.

## Open Questions

- O `scripts/seed.py` já existe e é idempotente? Verificar antes de executar no Neon.
- A connection string do Neon deve ser compartilhada com todos os membros via qual canal seguro? (Sugestão: Discord privado do time ou 1Password compartilhado.)
