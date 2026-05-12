# Kanban — Processo Produtivo

## Visão geral

Este documento define o fluxo de trabalho Kanban adotado pelo projeto, incluindo a descrição de cada coluna e suas regras de uso.

---

## Objetivo

Padronizar o fluxo de desenvolvimento para melhorar:

- Visibilidade das tarefas  
- Organização do trabalho  
- Eficiência do time  
- Qualidade das entregas  

---

## Conteúdo principal

### Estrutura do Kanban

#### 1. New

Ideias de itens novos já identificados, mas ainda não refinados.

Demandas aguardando análise e detalhamento.

---

#### 2. Backlog

Itens refinados, priorizados e prontos para desenvolvimento futuro. Também é o local onde os requisitos previstos são listados, servindo como base para seleção de tarefas em cada sprint.

Não fazem parte do sprint atual.

---

#### 3. Sprint Backlog

Itens selecionados para o sprint atual.

Representam o compromisso ativo do time.

---

#### 4. Em andamento

Itens em desenvolvimento ativo.

Código, design ou implementação em progresso.

---

#### 5. Em revisão

Itens finalizados em desenvolvimento e aguardando validação.

Inclui:

- Code review (Pull Request)  
- Testes (QA)  
- Validação funcional  

---

#### 6. Em documentação

Itens já validados, aguardando documentação final.

Inclui:

- Documentação técnica  
- Atualização de README  
- Registro de decisões  

---

#### 7. Pronto

Itens completamente finalizados e documentados.

Prontos para entrega, deploy ou publicação.

---

#### 8. Feito

Itens entregues e concluídos oficialmente.

Nenhuma ação adicional é necessária.

---

### Regras de transição

- Ideia → New: item identificado e precisa de análise  
- New → Backlog: item refinado e priorizado  
- Backlog → Sprint Backlog: item selecionado para sprint  
- Sprint Backlog → Em andamento: desenvolvimento iniciado  
- Em andamento → Em revisão: implementação concluída  
- Em revisão → Em documentação: item aprovado  
- Em documentação → Pronto: documentação finalizada  
- Pronto → Feito: item entregue ou deploy realizado  

---

## Conteúdo adicional

### Boas práticas

- Limitar tarefas em Em andamento (WIP limit)  
- Não pular etapas do fluxo  
- Garantir que toda tarefa em Feito esteja documentada  
- Manter descrições claras e atualizadas  

---

## Observações

Este fluxo pode evoluir conforme o time identifica melhorias no processo.

Revisões periódicas sã