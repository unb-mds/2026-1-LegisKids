---
name: gemini-ai-integration
description: Use this skill whenever integrating, calling, or debugging the Google Gemini API in the LegisKids backend — summarizing legislative text, classifying themes/impact, generating plain-language explanations of proposições, or any code that imports google-generativeai / google-genai. Triggers on "Gemini", "resumo automático", "IA generativa", "classificação por IA", or files in a services/ai or services/gemini module. For the Flask route exposing this functionality, also consult flask-backend.
---

# Integração com Google Gemini — LegisKids

## Papel da IA no produto

O Gemini é usado para tornar proposições legislativas mais acessíveis: resumir ementas longas em linguagem simples, classificar tema/impacto automaticamente, e possivelmente gerar explicações para o público infantil/jovem (dado o nome "LegisKids"). Trate a IA como uma camada de **enriquecimento de dados**, não como fonte de verdade — sempre guarde o texto original junto com o resultado gerado.

## Setup do SDK

```python
# requirements.txt
google-genai>=0.3.0
```

```python
# src/services/gemini_client.py
import os
from google import genai

_client: genai.Client | None = None

def get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.environ["GEMINI_API_KEY"]
        _client = genai.Client(api_key=api_key)
    return _client
```

Mantenha o client como singleton em vez de instanciar a cada chamada. Nunca hardcode a API key — sempre via variável de ambiente (`.env`, nunca commitado).

## Padrão de chamada com prompt estruturado

```python
# src/services/resumo_service.py
from src.services.gemini_client import get_client

MODELO = "gemini-2.0-flash"

def resumir_ementa(ementa: str) -> str:
    client = get_client()
    prompt = (
        "Resuma a ementa legislativa abaixo em até 3 frases, em linguagem simples, "
        "acessível para um leitor sem formação jurídica. Não invente informações que "
        "não estejam no texto original.\n\n"
        f"Ementa original:\n{ementa}"
    )
    resposta = client.models.generate_content(model=MODELO, contents=prompt)
    return resposta.text.strip()
```

Boas práticas de prompt para este domínio:
- Sempre instrua explicitamente "não invente informações que não estejam no texto" — crítico para conteúdo legislativo, onde alucinação é especialmente prejudicial.
- Peça formato de saída explícito (frases, JSON, lista) em vez de confiar no "jeito natural" do modelo responder.
- Para classificação (tema, impacto), peça saída estruturada e valide:

```python
import json

def classificar_tema(ementa: str) -> str:
    client = get_client()
    prompt = (
        "Classifique a proposição abaixo em exatamente um destes temas: "
        "Educação, Saúde, Meio Ambiente, Economia, Segurança, Outro.\n"
        "Responda apenas com JSON no formato {\"tema\": \"<tema>\"}.\n\n"
        f"Ementa:\n{ementa}"
    )
    resposta = client.models.generate_content(model=MODELO, contents=prompt)
    try:
        dados = json.loads(resposta.text)
        return dados["tema"]
    except (json.JSONDecodeError, KeyError):
        return "Outro"  # fallback seguro em vez de propagar erro de parsing
```

## Tratamento de erros e resiliência

A API externa pode falhar, ter rate limit, ou retornar lento. Nunca deixe uma chamada de IA travar uma rota síncrona sem timeout/fallback:

```python
import logging
from google.genai import errors as genai_errors

logger = logging.getLogger(__name__)

def resumir_com_fallback(ementa: str) -> str:
    try:
        return resumir_ementa(ementa)
    except genai_errors.APIError as e:
        logger.warning("Gemini API falhou: %s", e)
        return ementa[:280] + "..."  # fallback: trunca o texto original
```

- Para processamento em lote (resumir muitas proposições de uma vez), processe de forma assíncrona/em background (fila de tarefas ou script separado), não dentro do ciclo request/response do Flask.
- Cacheie resultados de IA por proposição (coluna no banco, ex.: `resumo_ia`, `tema_ia`) em vez de chamar o Gemini a cada requisição do usuário — economiza custo e latência.

## Custos e limites

- Use o modelo mais leve que atende o caso de uso (ex.: variantes "flash") para tarefas de resumo/classificação simples; reserve modelos maiores só se a qualidade do flash for insuficiente.
- Monitore volume de chamadas — processamento em lote de milhares de proposições pode gerar custo significativo; prefira processar incrementalmente (apenas proposições novas/atualizadas).

## Segurança e privacidade

- Nunca envie dados pessoais sensíveis de usuários da plataforma para o prompt — apenas o conteúdo público da proposição legislativa.
- Sanitize/trunque textos extremamente longos antes de enviar (defina um limite de caracteres) para evitar custo desnecessário e erros de contexto.

## Checklist

1. API key via variável de ambiente, client como singleton.
2. Prompt instrui explicitamente a não inventar informação.
3. Saída estruturada (JSON) validada com fallback seguro em caso de parsing falhar.
4. Erros da API tratados com fallback, nunca propagam como 500 cru para o usuário final.
5. Resultado de IA cacheado/persistido no banco, não recalculado a cada request.
6. Processamento em lote feito fora do ciclo request/response.
