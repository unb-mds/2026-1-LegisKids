# Uso do OpenSpec no Projeto de Métodos e Desenvolvimento de Software

O uso do OpenSpec no projeto tem como objetivo organizar melhor o processo de desenvolvimento, evitando que as funcionalidades sejam implementadas apenas com base em conversas soltas, ideias incompletas ou decisões não documentadas.

O OpenSpec permite que cada alteração do sistema seja planejada antes da implementação, por meio de arquivos como proposta, design, tarefas e especificações. Com isso, a equipe consegue entender claramente o que será feito, por que será feito, quais partes do sistema serão afetadas e quais etapas precisam ser executadas.

Esse framework também ajuda a manter o projeto mais alinhado com boas práticas de engenharia de software, pois registra os requisitos, decisões técnicas e mudanças feitas ao longo do desenvolvimento. Assim, o projeto se torna mais fácil de revisar, manter e evoluir.

Além disso, o OpenSpec facilita o trabalho em equipe, já que todos conseguem consultar a mesma documentação e acompanhar o andamento das mudanças. Isso reduz erros de comunicação, evita retrabalho e melhora a organização geral do projeto.

Portanto, o uso do OpenSpec se justifica por trazer mais clareza, padronização, rastreabilidade e controle para o desenvolvimento do software, tornando o processo mais profissional e compatível com os objetivos da disciplina.

## Tutorial rápido de uso do OpenSpec

Após o OpenSpec já estar instalado:

1. Abra o terminal na pasta do projeto.

2. Inicialize o OpenSpec no projeto:

```bash
openspec init
```

3. Crie uma proposta para uma nova funcionalidade ou alteração:

```bash
/opsx:propose "descreva aqui o que deseja implementar"
```

4. Revise os arquivos gerados na pasta:

```bash
openspec/changes/
```

Normalmente serão criados arquivos como:

```bash
proposal.md
design.md
tasks.md
spec.md
```

5. Após revisar e confirmar a proposta, implemente a mudança:

```bash
/opsx:apply
```

6. Quando a implementação estiver concluída, arquive a mudança:

```bash
/opsx:archive
```

7. Sempre que necessário, atualize as instruções do OpenSpec no projeto:

```bash
openspec update
```

Com esse fluxo, cada mudança passa por planejamento, revisão, execução e registro, mantendo o projeto mais organizado.
