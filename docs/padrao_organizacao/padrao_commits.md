# Padronização de Commits

## Visão geral

Os commits devem seguir um padrão consistente para facilitar o entendimento do histórico do projeto.

---

## Conteúdo principal

### Formato padrão

tipo: descrição breve da alteração

---

### Exemplos

- feat: adiciona tela de login  
- fix: corrige validação do formulário  
- docs: atualiza documentação da API  

---

### Prefixos oficiais

| Prefixo     | Uso                                         | Exemplo |
|------------|----------------------------------------------|--------|
| feat       | Nova funcionalidade                          | feat: adiciona cadastro de usuário |
| fix        | Correção de bug                              | fix: corrige erro na autenticação |
| refactor   | Refatoração sem alterar comportamento        | refactor: reorganiza service de login |
| docs       | Alterações na documentação                   | docs: adiciona guia de instalação |
| style      | Formatação de código ou estilo               | style: ajusta indentação do controller |
| test       | Adição ou ajuste de testes                   | test: adiciona testes do módulo de usuários |
| chore      | Manutenção geral                             | chore: atualiza dependências |
| infra      | Infraestrutura                               | infra: configura docker compose |
| devops     | Pipeline e deploy                            | devops: adiciona workflow do GitHub Actions |
| management | Gestão de processos                          | management: atualiza template de issue |

---

### Regras de uso

**Deve:**

- usar prefixo em minúsculo  
- descrição curta e objetiva  
- verbo no presente  
- sem ponto final  

Exemplos corretos:

- feat: adiciona endpoint de login  
- fix: corrige erro no banco  

**Não deve:**

- commits genéricos  
- mensagens vagas  
- mistura de idiomas  

Exemplos incorretos:

- update  
- mudanças  
- corrigi coisas  