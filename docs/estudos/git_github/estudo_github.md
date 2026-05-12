# Estudo Git / GitHub

---

## Conceito geral

Git é um sistema de controle de versão que registra alterações feitas no código ao longo do tempo. Ele permite acompanhar a evolução do projeto, identificar mudanças, autores e momentos em que cada modificação foi realizada.

O GitHub complementa o Git ao funcionar como uma plataforma remota para armazenamento de repositórios, facilitando o trabalho em equipe, o compartilhamento de código e o versionamento centralizado.

---

## Funcionamento do Git na prática

Durante o desenvolvimento, alterações são feitas continuamente no código, mas nem todas precisam ser salvas imediatamente.

O Git permite selecionar exatamente quais mudanças serão registradas por meio de commits.

Cada commit representa um estado do projeto em um determinado momento, formando um histórico completo de evolução do código.

Esse histórico permite:

- Voltar versões anteriores
- Comparar mudanças
- Entender a evolução do sistema
- Reduzir riscos de perda de código

---

## Estrutura do histórico

O Git organiza o projeto como uma sequência de versões encadeadas.

Cada commit armazena o estado do projeto naquele instante, permitindo controle total sobre o desenvolvimento.

Isso possibilita testar alterações com segurança, sabendo que é possível reverter mudanças quando necessário.

---

## Organização com branches

Branches permitem criar linhas paralelas de desenvolvimento.

A branch principal (main) representa a versão estável do projeto, enquanto outras branches são usadas para:

- Desenvolvimento de novas funcionalidades
- Correção de bugs
- Testes experimentais

Após finalização, as alterações são integradas à branch principal.

---

## Integração e conflitos

A integração entre branches ocorre por meio de merge.

Em alguns casos, podem ocorrer conflitos quando duas alterações afetam a mesma parte do código. Nesses casos, o desenvolvedor precisa decidir qual versão manter.

Esse processo é comum em equipes e faz parte do fluxo de desenvolvimento colaborativo.

---

## Papel do GitHub

O GitHub fornece uma interface remota para o Git, permitindo:

- Armazenamento centralizado do código
- Colaboração entre desenvolvedores
- Revisão de código por meio de Pull Requests
- Controle de versões acessível online

---

## Fluxo de trabalho

O fluxo básico de desenvolvimento com Git e GitHub segue as etapas:

1. Criação de uma branch para uma tarefa
2. Implementação das alterações
3. Registro das mudanças por commits
4. Envio para o repositório remoto
5. Abertura de Pull Request
6. Revisão de código
7. Merge para a branch principal

---

## Síntese

O Git é uma ferramenta de controle de versão que garante organização, segurança e rastreabilidade no desenvolvimento de software.

O GitHub complementa esse processo ao permitir colaboração, revisão e centralização do código em um ambiente remoto.

---

## Referência

https://git-scm.com/book/pt-br/v2