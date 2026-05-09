# Estudo sobre Login
Este documento tem o intuito de avaliar a forma de login atual do sistema, propor pelo menos 3 alternativas, e decidir a melhor para nosso projeto.

A ideia é que o login possibilite o usuário salvar projetos de lei, para ser notificado caso haja alguma atualização nele, consiga ter acesso ao seu histórico, etc.

Importante: o sistema trabalha apenas com **dados públicos**, e o login não envolve informações sensíveis, sendo utilizado apenas para personalização da experiência do usuário.

> **Identificar o usuário de forma simples e rápida**
> 

# Ideia 1: Login pelo Gov.br

## Prós:

- Alta confiabilidade e autenticação forte
- Identidade verificada do usuário
- Pode agregar credibilidade institucional ao sistema

## Contras:

- Complexidade alta de integração com o Governo do Brasil
- Processo burocrático para liberação de acesso
- Experiência do usuário mais lenta (redirecionamentos e validações)
- Totalmente desproporcional para o objetivo do sistema
- Pode afastar usuários devido à fricção no login

**Análise:** solução robusta demais para um problema simples.

# Ideia 2: Login pelo Google

## Prós:

- Implementação simples usando OAuth 2.0
- Experiência rápida e familiar
- Não exige criação de senha
- Alta taxa de adesão
- Baixa responsabilidade sobre segurança de credenciais
- Ideal para sistemas com dados não sensíveis

## Contras:

- Dependência de serviço externo (Google)
- Nem todos usuários possuem ou querem usar conta Google
- Menor controle sobre autenticação

**Análise:** excelente custo-benefício para o contexto do sistema.

# Ideia 3: Login próprio do sistema

## Prós:

- Total controle sobre usuários
- Independência de serviços externos
- Flexibilidade para evoluir funcionalidades
- Permite login com qualquer email

## Contras:

- Necessidade de implementar autenticação segura (hash, tokens, etc.)
- Implementar fluxo de recuperação de senha
- Maior esforço de desenvolvimento
- Responsabilidade maior com dados (mesmo sendo poucos)
- Pode gerar fricção (usuário precisa criar conta)

**Análise:** viável, mas exige mais trabalho do que o necessário inicialmente.

# Conclusão

Considerando que:

- os dados do sistema são públicos
- o login serve apenas para personalização (favoritos, histórico, notificações)
- não há necessidade de autenticação forte

→ A Ideia 1 (Gov.br) é **exagerada** para o contexto.

→ A Ideia 3 (login próprio) é **válida**, mas traz complexidade desnecessária no início do projeto.

→ A Ideia 2 (login pelo Google) oferece o melhor equilíbrio entre:

- simplicidade
- experiência do usuário
- baixo custo de implementação