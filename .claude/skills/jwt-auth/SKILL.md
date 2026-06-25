---
name: jwt-auth
description: Use this skill when implementing or debugging JWT-based session/authorization in the LegisKids Flask backend — issuing tokens after login (including after Google OAuth), validating tokens on protected routes, refresh tokens, or anything using PyJWT/flask-jwt-extended. Triggers on "JWT", "token de acesso", Authorization headers, or token expiration/refresh logic. For the Google login step that precedes token issuance, also consult google-oauth.
---

# JWT — Sessão e Autorização no LegisKids

## Papel do JWT no fluxo de auth

Depois que o login acontece (e-mail/senha tradicional ou Google OAuth, ver skill `google-oauth`), o backend emite um JWT próprio da aplicação — é esse token, não o `id_token` do Google, que a aplicação usa para autorizar chamadas subsequentes à API.

## Emitindo o token

```python
# requirements.txt
PyJWT>=2.8.0
```

```python
# src/services/jwt_service.py
import os
import jwt
import datetime

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITMO = "HS256"
EXPIRACAO_ACESSO = datetime.timedelta(hours=2)

def gerar_token_app(usuario) -> str:
    payload = {
        "sub": str(usuario.id),
        "email": usuario.email,
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "exp": datetime.datetime.now(datetime.timezone.utc) + EXPIRACAO_ACESSO,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITMO)
```

- `SECRET_KEY` vem de variável de ambiente, nunca hardcoded — e deve ser um valor longo e aleatório, diferente entre dev/produção.
- `exp` sempre presente — um JWT sem expiração é uma sessão que nunca pode ser revogada por tempo, apenas problemática.
- Não coloque dados sensíveis no payload: o JWT é apenas assinado, não criptografado — qualquer um pode decodificar e ler o conteúdo (só não pode alterar sem invalidar a assinatura).

## Validando o token em rotas protegidas

```python
# src/utils/auth_decorators.py
from functools import wraps
from flask import request, jsonify
import jwt
from src.services.jwt_service import SECRET_KEY, ALGORITMO

def requer_autenticacao(funcao):
    @wraps(funcao)
    def wrapper(*args, **kwargs):
        cabecalho = request.headers.get("Authorization", "")
        if not cabecalho.startswith("Bearer "):
            return jsonify({"error": "Token não informado"}), 401

        token = cabecalho.removeprefix("Bearer ").strip()
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITMO])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        request.usuario_id = payload["sub"]
        return funcao(*args, **kwargs)

    return wrapper
```

```python
# src/routes/perfil.py
from flask import Blueprint, jsonify, request
from src.utils.auth_decorators import requer_autenticacao

perfil_bp = Blueprint("perfil", __name__)

@perfil_bp.get("/")
@requer_autenticacao
def meu_perfil():
    usuario = buscar_usuario(request.usuario_id)
    return jsonify(usuario.to_dict()), 200
```

Sempre especifique `algorithms=[ALGORITMO]` explicitamente no `jwt.decode` — sem isso, versões antigas de bibliotecas JWT já foram vulneráveis a ataques de confusão de algoritmo (ex.: aceitar `alg: none` ou trocar HS256 por RS256 manipulando o header do token).

## Armazenamento do token no frontend

- Para a maioria dos casos, `localStorage` é aceitável dado a simplicidade, mas deixe claro que isso expõe o token a XSS — se houver qualquer vetor de injeção de script não sanitizado no frontend (ver skill `vanilla-frontend` sobre `innerHTML`), o token pode ser roubado.
- Alternativa mais segura quando o backend e o frontend estão no mesmo domínio (ou domínios configuráveis via cookie): cookie `httpOnly`, `secure`, `SameSite=Strict/Lax` — inacessível a JavaScript, mitigando XSS, mas exige atenção a CSRF.
- Envie o token sempre no header `Authorization: Bearer <token>`, nunca como query string (fica em logs de servidor/proxy e no histórico do navegador).

## Refresh tokens (se o projeto precisar de sessões longas)

Em vez de um único token de longa duração (risco maior se roubado), use o padrão de **access token curto + refresh token longo**:
- Access token: minutos/poucas horas de validade, usado em toda requisição.
- Refresh token: dias/semanas, armazenado de forma mais protegida (cookie `httpOnly`), usado apenas para obter um novo access token em um endpoint dedicado (`/api/auth/refresh`).
- Refresh tokens devem ser revogáveis (guardar uma referência/hash no banco) — um JWT puro não pode ser "invalidado" antes de expirar sem esse controle adicional.

## Erros comuns a evitar

- Comparar tokens com `==` simples não é o problema aqui (a biblioteca já valida a assinatura criptograficamente), mas nunca implemente verificação de assinatura "manual" — sempre use a biblioteca (`PyJWT`) para isso.
- Não decodificar o token sem verificar a assinatura (`jwt.decode(token, options={"verify_signature": False})`) em código de produção — isso aceita qualquer token, mesmo forjado.
- Não reaproveitar o `id_token` do Google como se fosse a sessão da aplicação — ele tem audience/expiração definidas pelo Google, não pela sua aplicação, e mistura dois sistemas de confiança diferentes.

## Checklist

1. `SECRET_KEY` forte, via variável de ambiente, diferente entre ambientes.
2. Todo token tem `exp`; nenhum payload contém dado sensível além do necessário para identificar o usuário.
3. `jwt.decode` sempre com `algorithms=[...]` explícito.
4. Rotas protegidas usando um decorator/middleware central, não checagem manual repetida em cada rota.
5. Se houver sessão de longa duração, usar par access/refresh token, com refresh revogável.
