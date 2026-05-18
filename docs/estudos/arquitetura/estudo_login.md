# Estudo sobre Login

Este documento tem como objetivo avaliar a forma de autenticação do sistema, propor alternativas viáveis e definir a abordagem mais adequada para o projeto.

O sistema permitirá que o usuário salve projetos de lei, acompanhe atualizações e acesse seu histórico.

Importante: o sistema trabalha apenas com dados públicos, e o login tem como finalidade exclusiva a personalização da experiência do usuário.

---

# Objetivo do login

- Identificar o usuário de forma simples e eficiente
- Permitir personalização (favoritos, histórico e notificações)
- Garantir boa experiência de uso

---

# Alternativas de login

## Ideia 1: Login com Gov.br

### Vantagens

- Alta confiabilidade e autenticação forte
- Identidade verificada do usuário
- Maior credibilidade institucional

### Desvantagens

- Integração complexa com o governo
- Processo burocrático para liberação de acesso
- Experiência do usuário mais lenta
- Complexidade desproporcional ao escopo do projeto
- Possível redução na adesão de usuários

### Análise

Solução robusta, porém excessiva para as necessidades do sistema.

---

## Ideia 2: Login com Google (OAuth 2.0)

### Vantagens

- Implementação simples
- Experiência rápida e familiar
- Não exige criação de senha
- Alta taxa de adesão
- Boa segurança sem gestão de credenciais
- Adequado para sistemas com dados não sensíveis

### Desvantagens

- Dependência de serviço externo
- Nem todos os usuários utilizam Google
- Menor controle sobre autenticação

### Análise

Solução com melhor equilíbrio entre simplicidade, usabilidade e custo de implementação.

---

## Ideia 3: Login próprio do sistema

### Vantagens

- Controle total sobre usuários
- Independência de serviços externos
- Flexibilidade para futuras melhorias
- Permite qualquer e-mail

### Desvantagens

- Maior complexidade de implementação
- Necessidade de segurança (hash, tokens, etc.)
- Sistema de recuperação de senha
- Maior responsabilidade sobre dados
- Mais fricção para o usuário

### Análise

Solução viável, porém mais complexa do que o necessário para o estágio atual do projeto.

---

# Conclusão

Considerando que:

- o sistema utiliza apenas dados públicos
- o login serve apenas para personalização
- não há necessidade de autenticação avançada

Conclui-se que:

- O login com Gov.br é excessivo para o escopo do projeto
- O login próprio adiciona complexidade desnecessária neste momento
- O login com Google (OAuth 2.0) apresenta o melhor equilíbrio entre simplicidade, usabilidade e esforço de implementação

Portanto, a alternativa mais adequada para o sistema é o login via Google.