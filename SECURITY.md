# SECURITY.md

# Política de Segurança — LegisKids

## Escopo

Esta política cobre o repositório **LegisKids** e os componentes relacionados ao projeto, incluindo:

* código-fonte da aplicação
* documentação
* API
* banco de dados
* dependências
* configurações de ambiente

---

## Reportando Vulnerabilidades

**Não abra issues públicas para relatar vulnerabilidades de segurança.**

Caso encontre:

* falhas de segurança
* exposição de dados
* vulnerabilidades
* comportamento suspeito

entre em contato de forma privada com os mantenedores do projeto.

O reporte deve incluir:

* descrição clara da vulnerabilidade
* passos para reprodução
* impacto potencial
* versão, commit ou arquivo afetado

---

## Processo de Resposta

A equipe do projeto buscará:

* confirmar o recebimento do reporte
* avaliar o impacto do problema
* trabalhar na correção o mais rápido possível
* manter o reportador informado sobre o andamento

---

## Boas Práticas para Contribuidores

### Credenciais e Segredos

* Nunca commitar senhas, tokens ou chaves de API
* Utilizar variáveis de ambiente para informações sensíveis
* Não expor arquivos `.env`
* Verificar arquivos antes de abrir Pull Requests

---

### Dependências

Ao adicionar novas dependências:

* verificar compatibilidade com o projeto
* evitar bibliotecas abandonadas
* revisar possíveis vulnerabilidades conhecidas

Exemplo:

```bash id="a5j2r4"
pip audit
```

---

### Dados Sensíveis

* Não utilizar dados reais em testes
* Preferir dados fictícios ou anonimizados
* Evitar exposição de informações pessoais

---

## Versões Suportadas

Correções de segurança serão priorizadas para a branch principal de desenvolvimento ativa (`develop`) e versões estáveis derivadas da `main`.

---

## Divulgação Responsável

Após a correção de uma vulnerabilidade, os detalhes poderão ser divulgados pela equipe responsável, respeitando a segurança do projeto e dos usuários.
