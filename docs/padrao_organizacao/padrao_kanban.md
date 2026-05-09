# Kanban — Processo Produtivo

Este documento define o fluxo de trabalho Kanban adotado pelo projeto, incluindo a descrição de cada coluna e regras básicas de uso.

## Objetivo

Padronizar o fluxo de desenvolvimento para melhorar:

- Visibilidade das tarefas
- Organização do trabalho
- Eficiência do time
- Qualidade das entregas

## Estrutura do Kanban

### 1. New

Ideias de itens novos já identificados, mas ainda não refinados.

> Demandas aguardando análise e detalhamento.
> 

### 2. Backlog

Itens refinados, priorizados e prontos para desenvolvimento futuro.  
Também será onde os requisitos previstos estarão listados, e de onde puxaramos para decidir o que fazer em cada Sprint.

> Não fazem parte do sprint atual.
> 

### 3. Sprint Backlog

Itens selecionados para o sprint atual.

> Representam o compromisso ativo do time.
> 

### 4. Em andamento

Itens em desenvolvimento ativo.

> Código, design ou implementação em progresso.
> 

### 5. Em Revisão

Itens finalizados em desenvolvimento e aguardando validação.

> Inclui:
> 
- Code Review (PR)
- Testes (QA)
- Validação funcional

### 6. Em Documentação

Itens já validados, aguardando documentação.

> Inclui:
> 
- Documentação técnica
- Atualização de README
- Registro de decisões

### 7. Pronto

Itens completamente finalizados e documentados.

> Prontos para deploy, entrega ou publicação.
> 

### 9. Feito

Itens entregues e concluídos oficialmente.

> Nenhuma ação adicional necessária.
> 

## Regras de Transição

- **IDEIA → New:** Item foi identificado e precisa de análise
- **New → Backlog:** Item foi refinado e priorizado
- **Backlog → Sprint Backlog:** Item selecionado para o sprint
- **Sprint Backlog → Em andamento:** Desenvolvimento iniciado
- **Em andamento → Em Revisão:** Implementação concluída
- **Em Revisão → Em Documentação:** Item aprovado
- **Em Documentação → Pronto:** Documentação finalizada
- **Pronto → Feito:** Item entregue/deploy realizado

## Boas Práticas

- Limitar tarefas em **Em andamento** (WIP Limit)
- Não pular etapas do fluxo
- Garantir que toda tarefa em **Done** esteja documentada
- Manter descrições claras e atualizadas

## Observações

Este fluxo pode evoluir conforme o time identifica melhorias no processo.

Revisões periódicas são recomendadas para manter a eficiência do Kanban.