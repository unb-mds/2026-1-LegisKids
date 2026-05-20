# SDD — Spec-Driven Development

## 1. O que é SDD?

**SDD**, ou **Spec-Driven Development**, é o **desenvolvimento orientado por especificações**.

A ideia principal é simples:

> Antes de programar, escreva claramente o que deve ser construído.

Em vez de começar direto pelo código, você primeiro cria uma **spec**: um documento curto e objetivo que explica o problema, o objetivo, o escopo, os requisitos, os critérios de aceitação e os testes esperados.

---

## 2. Por que SDD é útil?

SDD ajuda a evitar que uma tarefa fique vaga demais.

Pedido ruim:

```text
Melhore o sistema.
```

Pedido melhor:

```text
Criar autenticação por e-mail e senha, com validação de campos, mensagens de erro, proteção de senha e redirecionamento após login. Não alterar o fluxo de cadastro já existente.
```

A segunda versão é melhor porque deixa claro:

- o que deve ser feito;
- o que deve ser preservado;
- qual comportamento é esperado;
- onde termina a tarefa.

---

## 3. SDD em uma frase

```text
Spec → Plano → Tarefas → Código → Testes → Validação
```

O código deixa de ser o primeiro passo.  
A especificação passa a guiar a implementação.

---

## 4. Diferença entre prompt comum e SDD

### Prompt comum

```text
Faça uma página de vendas bonita.
```

Problema: o pedido é subjetivo.

### SDD

```text
Criar uma landing page para venda de um curso online.

A página deve conter:
- seção principal com título, subtítulo e botão de compra;
- seção de benefícios;
- seção de depoimentos;
- seção de preço;
- FAQ;
- botão final de chamada para ação.

Não implementar sistema de pagamento. Apenas criar a interface.
```

Resultado: o escopo fica claro e a IA/desenvolvedor tem menos margem para interpretar errado.

---

## 5. O que uma boa spec precisa ter?

Uma boa `spec.md` deve conter:

1. **Objetivo**  
   O que será feito.

2. **Contexto**  
   Qual é o problema atual.

3. **Escopo**  
   O que entra e o que não entra na tarefa.

4. **Requisitos**  
   O que o sistema precisa fazer.

5. **Critérios de aceitação**  
   Como saber que a tarefa ficou pronta.

6. **Testes**  
   Como validar se funciona.

7. **Restrições**  
   O que não pode ser alterado ou quebrado.

---

## 6. Modelo rápido de spec.md

```markdown
# SPEC: Nome da tarefa

## Objetivo

Explique de forma direta o que deve ser feito.

## Contexto

Explique o problema atual ou a necessidade.

## Escopo

### Fazer

- Item 1
- Item 2
- Item 3

### Não fazer

- Não alterar X
- Não refatorar Y
- Não criar Z

## Requisitos

- O sistema deve...
- A interface deve...
- O usuário deve conseguir...

## Critérios de aceitação

- [ ] Critério objetivo 1
- [ ] Critério objetivo 2
- [ ] Critério objetivo 3

## Testes

- Testar cenário normal.
- Testar erro.
- Testar caso vazio.
- Testar limite.
```

---

## 7. Exemplo geral de spec

```markdown
# SPEC: Sistema de recuperação de senha

## Objetivo

Implementar um fluxo de recuperação de senha por e-mail.

## Contexto

Usuários que esquecem a senha atualmente não conseguem recuperar o acesso sem suporte manual.

## Escopo

### Fazer

- Criar tela para solicitar recuperação de senha.
- Enviar e-mail com link temporário.
- Criar tela para definir nova senha.
- Validar força mínima da nova senha.
- Exibir mensagens de erro e sucesso.

### Não fazer

- Não alterar o fluxo de login atual.
- Não alterar o fluxo de cadastro.
- Não implementar autenticação social.
- Não modificar permissões de usuário.

## Requisitos

- O link de recuperação deve expirar.
- A nova senha deve ser validada antes de salvar.
- O usuário deve receber mensagem clara após solicitar recuperação.
- O token não deve poder ser reutilizado.

## Critérios de aceitação

- [ ] Usuário consegue solicitar recuperação informando o e-mail.
- [ ] Sistema envia link de recuperação.
- [ ] Link expirado não permite redefinir senha.
- [ ] Token usado não pode ser reutilizado.
- [ ] Usuário consegue entrar com a nova senha.
- [ ] Login, cadastro e permissões continuam funcionando.

## Testes

- Testar e-mail válido.
- Testar e-mail inexistente.
- Testar token expirado.
- Testar token já usado.
- Testar senha fraca.
- Testar senha válida.
```

---

## 8. Quando usar SDD?

Use SDD principalmente quando a tarefa envolve:

- múltiplos arquivos;
- regras de negócio;
- autenticação;
- pagamentos;
- banco de dados;
- APIs;
- permissões;
- interface importante;
- refatoração;
- uso de IA para programar;
- manutenção de código existente;
- risco de quebrar funcionalidades antigas.

Para tarefas muito pequenas, uma spec curta já basta.

---

## 9. Benefícios do SDD

SDD ajuda a:

- reduzir retrabalho;
- melhorar comunicação;
- evitar mudanças fora do escopo;
- guiar agentes de IA;
- documentar decisões;
- criar critérios claros de conclusão;
- facilitar revisão de código;
- preservar regras importantes do projeto;
- diminuir ambiguidades.

---

## 10. Erros comuns ao usar SDD

Evite:

- spec grande demais;
- misturar várias tarefas em uma spec;
- não definir o que está fora do escopo;
- não criar critérios de aceitação;
- usar termos vagos como “melhorar”, “otimizar” ou “arrumar” sem explicar;
- pedir implementação antes de revisar a spec;
- não atualizar a spec quando o plano muda.

---

# 11. Frameworks e ferramentas de Spec-Driven Development

Além de escrever specs manualmente, existem ferramentas que ajudam a organizar esse fluxo.

Elas normalmente criam uma estrutura como:

```text
specs/
changes/
tasks/
plans/
docs/
```

A função dessas ferramentas é transformar uma ideia em um processo mais controlado:

```text
Ideia → Proposta → Spec → Tarefas → Implementação → Validação
```

---

## 12. OpenSpec

**OpenSpec** é um framework leve de SDD voltado para uso com agentes de programação e CLIs.

Ele ajuda a transformar pedidos em propostas, mudanças e especificações versionadas.

A ideia central do OpenSpec é:

> Travar a intenção antes da implementação.

Ou seja, antes da IA sair alterando o código, o projeto passa por uma etapa de proposta/spec.

Um fluxo comum do OpenSpec é:

```text
propose → apply → archive
```

### Como pensar no OpenSpec

O OpenSpec funciona como uma camada de organização entre você e o agente de IA.

Em vez de pedir:

```text
Implemente essa funcionalidade.
```

Você segue um fluxo mais seguro:

```text
1. Criar proposta da mudança
2. Revisar o que será feito
3. Aprovar ou ajustar a spec
4. Implementar
5. Arquivar a mudança concluída
```

### Quando OpenSpec é útil?

OpenSpec é útil quando:

- você já tem um projeto existente;
- quer evitar mudanças soltas;
- quer registrar decisões;
- quer trabalhar com agentes de IA;
- precisa revisar a intenção antes da implementação;
- quer manter histórico das mudanças;
- quer separar proposta, tarefa e implementação.

### Vantagem principal

O OpenSpec é especialmente interessante para projetos existentes, porque trabalha bem com mudanças incrementais.

Em vez de exigir uma especificação gigante de todo o sistema, ele pode organizar mudanças menores por proposta.

### Instalação básica

```bash
npm install -g @fission-ai/openspec@latest
```

> Observação: se der erro, confira se o Node.js e o npm estão atualizados e se o comando não tem caracteres extras, como `~` no final.

---

## 13. GitHub Spec Kit

**GitHub Spec Kit** é um toolkit para SDD criado para fluxos com agentes de IA.

Ele propõe que você defina o que será construído antes de escrever código.

O foco dele é estruturar o desenvolvimento em fases, como:

```text
Specify → Plan → Tasks → Implement
```

Ou seja:

1. **Specify**: definir o que será feito.
2. **Plan**: planejar como será feito.
3. **Tasks**: quebrar em tarefas.
4. **Implement**: executar a implementação.

### Quando o GitHub Spec Kit é útil?

Ele é útil quando:

- você está começando um projeto novo;
- precisa organizar um fluxo completo de IA;
- quer padronizar specs, planos e tarefas;
- quer integrar com agentes como Copilot, Claude Code ou Gemini CLI;
- quer transformar uma ideia inicial em projeto estruturado.

### Diferença prática entre OpenSpec e Spec Kit

| Ferramenta | Melhor uso |
|---|---|
| OpenSpec | Mudanças incrementais em projetos existentes |
| GitHub Spec Kit | Projetos novos ou funcionalidades maiores com fluxo completo |
| Spec manual | Tarefas simples ou quando você não quer instalar ferramenta |

---

## 14. Outras ferramentas e abordagens relacionadas

Além de OpenSpec e GitHub Spec Kit, existem outras abordagens próximas:

### PRD

**Product Requirements Document**.  
Documento de requisitos de produto.

Costuma responder:

- quem é o usuário;
- qual problema será resolvido;
- qual valor será entregue;
- quais funcionalidades são necessárias.

### ADR

**Architecture Decision Record**.  
Documento curto para registrar decisões técnicas.

Exemplo:

```text
Decisão: usar PostgreSQL em vez de MongoDB.
Motivo: precisamos de relações fortes entre usuários, pedidos e pagamentos.
Consequências: maior consistência, porém menos flexibilidade documental.
```

### RFC

**Request for Comments**.  
Documento usado para propor uma mudança e receber comentários antes da implementação.

### User Stories

Formato comum em times ágeis:

```text
Como usuário, quero recuperar minha senha para voltar a acessar minha conta.
```

### BDD

**Behavior-Driven Development**.  
Descreve comportamento esperado em cenários:

```gherkin
Dado que o usuário esqueceu a senha
Quando ele solicita recuperação
Então deve receber um link por e-mail
```

SDD pode usar PRD, ADR, RFC, User Stories e BDD dentro da própria spec.

---

## 15. SDD manual vs SDD com framework

### SDD manual

Você cria um arquivo `spec.md` e organiza tudo sozinho.

Bom para:

- tarefas pequenas;
- projetos pessoais;
- ajustes rápidos;
- uso simples com IA.

### SDD com framework

Você usa uma ferramenta como OpenSpec ou Spec Kit para organizar o processo.

Bom para:

- projetos maiores;
- times;
- tarefas críticas;
- histórico de mudanças;
- múltiplos agentes;
- revisão antes da implementação.

---

## 16. Exemplo de estrutura simples

```text
project/
  specs/
    password-reset/
      spec.md
      tasks.md
      plan.md

  src/
  tests/
  README.md
```

---

## 17. Exemplo de estrutura com OpenSpec

```text
project/
  openspec/
    project.md
    specs/
    changes/
      add-password-reset/
        proposal.md
        tasks.md
        spec.md
```

A ideia é manter as mudanças organizadas por proposta.

---

## 18. Exemplo de estrutura com Spec Kit

```text
project/
  specs/
    001-password-reset/
      spec.md
      plan.md
      tasks.md
```

A ideia é passar por fases claras: especificar, planejar, quebrar em tarefas e implementar.

---

## 19. Prompt recomendado para usar com IA

```text
Leia a spec antes de alterar qualquer arquivo.

Implemente somente o que está dentro do escopo.
Não refatore sistemas fora do escopo.
Não crie sistemas paralelos.
Preserve a lógica existente sempre que possível.

Antes de codar:
1. identifique os arquivos afetados;
2. explique o plano de alteração;
3. confirme como cada requisito será atendido.

Depois de implementar:
1. liste os arquivos alterados;
2. explique como cada mudança atende aos critérios de aceitação;
3. informe limitações ou pontos que precisam de validação manual.
```

---

## 20. Checklist rápido de uma boa spec

Antes de enviar a spec para uma IA ou equipe, confira:

```text
[ ] O objetivo está claro?
[ ] O problema atual foi explicado?
[ ] O escopo foi delimitado?
[ ] Está claro o que não deve ser alterado?
[ ] Existem requisitos objetivos?
[ ] Existem critérios de aceitação?
[ ] Existe plano de teste?
[ ] A spec tem uma tarefa principal, e não várias misturadas?
[ ] A linguagem está direta?
```

---

## 21. Resumo final

SDD é uma forma de desenvolver com mais clareza e controle.

A lógica é:

```text
Não peça código primeiro.
Peça uma especificação clara.
Revise a intenção.
Depois implemente.
```

Para projetos simples, um `spec.md` manual já resolve.

Para projetos maiores, ferramentas como **OpenSpec** e **GitHub Spec Kit** ajudam a organizar propostas, planos, tarefas e validação.

> SDD não é burocracia. É uma forma de evitar retrabalho, reduzir ambiguidade e fazer humanos e IAs trabalharem com o mesmo entendimento.

---

# Referências

- OpenSpec: https://openspec.dev/
- Repositório OpenSpec: https://github.com/Fission-AI/OpenSpec
- GitHub Spec Kit: https://github.github.com/spec-kit/
- Repositório GitHub Spec Kit: https://github.com/github/spec-kit
- GitHub Blog sobre Spec-Driven Development: https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
- Thoughtworks Technology Radar — OpenSpec: https://www.thoughtworks.com/radar/tools/openspec