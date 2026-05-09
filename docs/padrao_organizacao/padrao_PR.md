 📘 Guia Completo: Como Fazer um Pull Request (PR)

## 🎯 Contexto

Parte do time ainda não segue um fluxo padronizado de Pull Requests, o que pode gerar:

- conflitos de código  
- branches desorganizadas  
- dificuldade na revisão  

Este guia resolve isso com um fluxo simples e direto.

---

## 🚀 1. O que é um Pull Request (PR)?

Um **Pull Request (PR)** é uma solicitação para integrar alterações de uma branch para outra, geralmente para `main` ou `develop`.

> “Terminei minha feature, podem revisar e juntar no projeto?”

### ✅ Por que isso é importante?

- Permite revisão de código  
- Evita bugs entrarem direto na `main`  
- Mantém histórico organizado  
- Facilita trabalho em equipe  

---

## 🔄 2. Fluxo Completo (Passo a Passo)

### 🧩 Etapa 1 — Criar uma branch

Sempre trabalhe em uma branch separada da `main`.

```bash
git checkout -b feature/nome-da-feature

---

### ✍️ Etapa 2 — Fazer alterações

Implemente sua funcionalidade ou correção.

---

### ✅ Etapa 3 — Commitar

```bash
git add .
git commit -m "feat: adiciona sistema de inventário"
```

---

### ☁️ Etapa 4 — Dar push

```bash
git push origin feature/nome-da-feature
```

---

### 🔗 Etapa 5 — Abrir o PR no GitHub

1. Vá no repositório
2. Clique em **Compare & Pull Request**
3. Preencha título e descrição
4. Escolha:

   * `base`: `main` ou `develop`
   * `compare`: sua branch

---

### 👀 Etapa 6 — Revisão

* Outros membros analisam
* Podem pedir mudanças
* Você ajusta e faz novos commits

---

### 🟢 Etapa 7 — Merge

Após aprovação:

* Clique em **Merge Pull Request**
* Delete a branch (recomendado)

---

## 📂 3. Padronização de Branches (OBRIGATÓRIO)

### 📌 Formato padrão

```text
tipo/numero-issue-nome-curto
```

### 📌 Exemplos

```text
feature/12-sistema-loja
fix/34-bug-bau-duplicando
refactor/22-organizacao-modulos
hotfix/45-crash-servidor
```

### 🧠 Tipos de branch

| Tipo     | Uso                 |
| -------- | ------------------- |
| feature  | Nova funcionalidade |
| fix      | Correção de bug     |
| refactor | Melhorias internas  |
| hotfix   | Correção urgente    |
| docs     | Documentação        |

---

## 📝 4. Padronização de Commits

### 📌 Formato

```text
tipo: descrição curta
```

### 📌 Exemplos

```text
feat: adiciona sistema de mineração
fix: corrige bug do baú duplicando
refactor: melhora organização do código
docs: adiciona guia de PR
```

---

## 🔀 5. Padronização de Pull Requests

### 📌 Título do PR

```text
[tipo] #numero-issue - descrição curta
```

### 📌 Exemplos

```text
[feature] #12 - sistema de loja
[fix] #34 - correção do bug do baú
```

---

### 📄 Modelo de Descrição do PR

Copie e cole sempre:

```markdown
## 📌 O que foi feito?

- Descreva as alterações

## 🎯 Por que isso foi feito?

- Explique o objetivo

## 🧪 Como testar?

- Passo a passo para validar

## 📸 Prints/Vídeos (se houver)

## 🔗 Issue relacionada

Closes #numero
```

---

## ⚠️ 6. Boas Práticas (CRÍTICO)

* ❌ Nunca commitar direto na `main`
* ✅ Sempre usar branch
* ✅ Fazer PR mesmo sendo simples
* ✅ Manter PR pequeno (fácil de revisar)
* ✅ Nome claro em tudo (branch, commit, PR)
* ✅ Sempre linkar Issue

---

## 💡 7. Dicas de Ouro

* 1 PR = 1 objetivo (não misturar coisas)
* Prefira commits pequenos e frequentes
* Sempre puxe a `main` antes de começar:

```bash
git checkout main
git pull
```

---

## 🧾 Resumo Final

✔ Trabalhe em branch
✔ Faça commits claros
✔ Abra PR
✔ Passe por revisão
✔ Só depois faça merge

---

🚀 Seguindo esse padrão, o projeto fica organizado, escalável e muito mais profissional.

```

---

Se quiser dar um nível **ainda mais profissional**, posso te mandar:
- :contentReference[oaicite:0]{index=0}
- :contentReference[oaicite:1]{index=1}
- ou :contentReference[oaicite:2]{index=2} (pra site bonito)

Só falar 👍
```
