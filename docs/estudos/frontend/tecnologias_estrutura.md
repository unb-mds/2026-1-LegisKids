# Estudo: Front-End

## Tecnologias escolhidas

- HTML para estruturação das páginas
- CSS para estilização e organização visual
- JavaScript puro para lógica e manipulação do DOM
- Fetch API para comunicação com o back-end

A escolha por JavaScript puro foi feita para evitar complexidade inicial com frameworks, permitindo maior entendimento do funcionamento básico da aplicação.

---

## Integração com o back-end

O back-end será desenvolvido em Python com Flask, responsável por disponibilizar rotas seguindo o padrão de API REST. Essas rotas retornarão dados em JSON, consumidos diretamente pelo front-end via requisições HTTP, utilizando principalmente os métodos GET e POST.

Essa abordagem permite desacoplamento entre front-end e back-end, mesmo estando inicialmente no mesmo projeto.

---

## Funcionamento da comunicação

O fluxo básico da aplicação será:

1. O usuário acessa a interface (HTML)
2. O JavaScript executa uma requisição para o back-end (ex: `/api/dados`)
3. O Flask processa a requisição e retorna uma resposta em JSON
4. O front-end interpreta os dados recebidos
5. A interface é atualizada dinamicamente sem recarregar a página

Isso permite criar aplicações mais dinâmicas e interativas, mesmo sem o uso de frameworks modernos.

---

## Estrutura inicial (Flask)

```
templates/
└── index.html

static/
├── style.css
└── script.js
```

---

## Considerações

A decisão por essa stack foi baseada na necessidade de iniciar o desenvolvimento de forma simples, compreendendo bem a comunicação entre as partes antes de adotar soluções mais complexas. Essa abordagem também facilita manutenção, testes e futuras melhorias, permitindo que o projeto evolua de forma estruturada conforme novas demandas surgirem.

---

## Resumo

O estudo envolveu a análise de como ocorre a comunicação entre front-end e back-end, com foco no uso de APIs REST e troca de dados em JSON. Foram avaliadas diferentes tecnologias considerando nível de complexidade e adequação ao momento do projeto.

Com base nisso, foi definida uma abordagem com HTML, CSS e JavaScript no front-end, integrados a um back-end em Flask, garantindo uma base sólida para o desenvolvimento inicial.