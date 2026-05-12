# Labels de Tamanho das Issues

## Objetivo

Definir um padrão de classificação das Issues do projeto utilizando labels de tamanho para facilitar:

- planejamento das sprints
- distribuição de tarefas
- identificação de complexidade
- previsibilidade de entrega
- divisão de tarefas grandes em subtarefas menores

---

## Padrão de tamanhos

Cada Issue deverá receber uma label de tamanho:

| Label | Esforço | Tempo estimado | Complexidade |
| --- | --- | --- | --- |
| XS | Muito baixo | até 1 hora | simples |
| S | Baixo | 1 a 4 horas | pequena |
| M | Médio | 4 a 8 horas | moderada |
| L | Alto | 1 a 2 dias | complexa |
| XL | Muito alto | acima de 2 dias | muito complexa |

---

## Critérios para classificação

### XS

Ajuste simples, correção visual pequena, alteração pontual ou documentação curta.

Exemplo: corrigir texto, alterar cor de botão, ajustar label.

---

### S

Pequena implementação, bug simples ou pequena melhoria.

Exemplo: criar endpoint simples, ajustar validação.

---

### M

Funcionalidade média, integração simples ou alteração em múltiplos arquivos.

Exemplo: criar formulário completo com validação.

---

### L

Funcionalidade importante, integração com banco ou API, impacto em várias partes do sistema.

Exemplo: implementar autenticação.

---

### XL

Tarefa muito grande, alto risco técnico ou necessidade de divisão.

Exemplo: módulo completo novo.

Sempre que possível, uma Issue XL deve ser dividida em Issues menores ou designada para mais de um integrante.

---

## Cores

As cores seguem uma lógica visual de esforço crescente:

- **XS** — verde claro
- **S** — verde
- **M** — amarelo
- **L** — laranja
- **XL** — vermelho

Verde representa menor esforço, amarelo o médio e vermelho o maior, facilitando a leitura rápida do backlog.

---

## Processo de uso

Ao criar uma nova Issue:

1. Criar a Issue normalmente
2. Avaliar esforço estimado
3. Aplicar label de tamanho
4. Validar com a equipe se necessário
5. Se for XL, considerar quebrar em subtarefas ou designar mais integrantes

---

## Definição da label

A label será definida pelo autor da Issue inicialmente, revisada durante o planning e validada pela equipe na mesma cerimônia.