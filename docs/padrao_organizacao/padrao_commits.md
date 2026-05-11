# Padronização de Commits
## Formato padrão

```
tipo: descrição breve da alteração
```

### Exemplo

```
feat: adiciona tela de login
fix: corrige validaçãodo formulário
docs: atualiza documentação da API
```

# Prefixos oficiais

| Prefixo | Uso | Exemplo |
| --- | --- | --- |
| `feat` | Nova funcionalidade | `feat: adiciona cadastro de usuário` |
| `fix` | Correção de bug | `fix: corrige erro na autenticação` |
| `refactor` | Refatoração sem mudar comportamento | `refactor: reorganiza service de login` |
| `docs` | Alterações na documentação | `docs: adiciona guia de instalação` |
| `style` | Formatação visual/código | `style: ajusta identação do controller` |
| `test` | Testes | `test: adiciona testes do módulo de usuários` |
| `chore` | Manutenção geral | `chore: atualiza dependências` |
| `infra` | Infraestrutura | `infra: configura docker compose` |
| `devops` | Pipeline/deploy | `devops: adiciona workflow do github actions` |
| `management` | Gestão/processos | `management: atualiza template de issue` |

# Regras de uso

## Deve:

- usar prefixo em minúsculo
- descrição curta
- verbo no presente
- sem ponto final

### Correto

```
feat: adiciona endpoint de login
fix: corrige erro no banco
```

## Não deve:

- commits genéricos
- mensagens vagas
- mistura de idiomas

### Incorreto

```
update
mudanças
corrigi coisas
```