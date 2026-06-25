---
name: google-oauth
description: Use this skill when implementing or debugging "Sign in with Google" / Google OAuth 2.0 login in the LegisKids project, on either the Flask backend (token verification, OAuth callback) or the frontend (Google Identity Services button/flow). Triggers on "login com Google", "Google OAuth", "Google Sign-In", client_id, or id_token verification code. For issuing the app's own session tokens after Google login succeeds, also consult jwt-auth.
---

# Google OAuth — Login com Google no LegisKids

## Fluxo recomendado: Google Identity Services + verificação no backend

Para uma SPA (Vue) ou página vanilla, o caminho mais simples e seguro é usar o **Google Identity Services (GIS)** no frontend para obter um `id_token`, e validar esse token no backend Flask — evita o backend precisar gerenciar todo o fluxo de redirecionamento OAuth manualmente.

### Frontend — botão de login

```html
<script src="https://accounts.google.com/gsi/client" async defer></script>
<div id="g_id_onload"
     data-client_id="SEU_CLIENT_ID.apps.googleusercontent.com"
     data-callback="aoLogarComGoogle">
</div>
<div class="g_id_signin" data-type="standard"></div>
```

```javascript
async function aoLogarComGoogle(resposta) {
  // resposta.credential é o id_token JWT assinado pelo Google
  const resultado = await fetch("/api/auth/google", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id_token: resposta.credential }),
  });

  if (!resultado.ok) {
    console.error("Falha no login com Google");
    return;
  }

  const { token } = await resultado.json();
  // token aqui é o JWT da própria aplicação — ver skill jwt-auth
  localStorage.setItem("token_app", token);
}

window.aoLogarComGoogle = aoLogarComGoogle;
```

Em Vue, o mesmo padrão se aplica dentro de um componente, geralmente carregando o script do GIS no `onMounted` e expondo `aoLogarComGoogle` via `window` ou callback configurado dinamicamente.

### Backend — verificação do id_token

```python
# requirements.txt
google-auth>=2.0.0
```

```python
# src/services/google_auth_service.py
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

GOOGLE_CLIENT_ID = "SEU_CLIENT_ID.apps.googleusercontent.com"

def verificar_token_google(token: str) -> dict:
    """Valida o id_token do Google e retorna os dados do usuário.

    Lança ValueError se o token for inválido, expirado, ou de outra audience.
    """
    info = id_token.verify_oauth2_token(
        token, google_requests.Request(), audience=GOOGLE_CLIENT_ID
    )

    if info["iss"] not in ("accounts.google.com", "https://accounts.google.com"):
        raise ValueError("Issuer inválido")

    return {
        "google_id": info["sub"],
        "email": info["email"],
        "nome": info.get("name"),
        "avatar_url": info.get("picture"),
        "email_verificado": info.get("email_verified", False),
    }
```

```python
# src/routes/auth.py
from flask import Blueprint, request, jsonify
from src.services.google_auth_service import verificar_token_google
from src.services.usuario_service import obter_ou_criar_usuario
from src.services.jwt_service import gerar_token_app

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/google")
def login_google():
    dados = request.get_json(force=True)
    id_token_recebido = dados.get("id_token")
    if not id_token_recebido:
        return jsonify({"error": "id_token é obrigatório"}), 400

    try:
        info_google = verificar_token_google(id_token_recebido)
    except ValueError:
        return jsonify({"error": "Token do Google inválido"}), 401

    if not info_google["email_verificado"]:
        return jsonify({"error": "E-mail do Google não verificado"}), 403

    usuario = obter_ou_criar_usuario(info_google)
    token_app = gerar_token_app(usuario)

    return jsonify({"token": token_app, "usuario": usuario.to_dict()}), 200
```

## Pontos críticos de segurança

- **Sempre valide o `id_token` no backend** com `id_token.verify_oauth2_token` — nunca confie em dados que o frontend "diz" terem vindo do Google sem essa verificação criptográfica, pois o frontend pode ser manipulado por um atacante.
- Sempre confira `audience` (seu `client_id`) e `issuer` — sem isso, um token válido emitido para outra aplicação Google poderia ser aceito indevidamente.
- Verifique `email_verified` antes de criar conta automaticamente a partir do e-mail do Google.
- O `client_id` pode ser público (vai no HTML/JS do frontend), mas nunca exponha um *client secret* no frontend — o fluxo de GIS com `id_token` não precisa de client secret no backend para esse caso de uso.

## Vinculando com a conta existente

Ao criar/buscar o usuário, use o `google_id` (campo `sub` do token) como identificador estável, não o e-mail isoladamente — e-mails podem ser reaproveitados ou alterados:

```python
def obter_ou_criar_usuario(info_google: dict):
    usuario = Usuario.query.filter_by(google_id=info_google["google_id"]).first()
    if usuario is None:
        usuario = Usuario(
            google_id=info_google["google_id"],
            email=info_google["email"],
            nome=info_google["nome"],
        )
        db.session.add(usuario)
        db.session.commit()
    return usuario
```

## Configuração no Google Cloud Console

- Registrar as origens JavaScript autorizadas (`http://localhost:5173` em dev, domínio real em produção) na tela de credenciais OAuth.
- Manter `client_id` em variável de ambiente também no frontend (build-time, via Vite `import.meta.env`), não hardcoded em múltiplos arquivos.

## Checklist

1. `id_token` sempre verificado no backend com `audience` e `issuer` checados.
2. `email_verified` confirmado antes de criar conta nova.
3. `google_id` (não e-mail) usado como chave de vínculo da conta.
4. Nenhum client secret exposto no frontend.
5. Após validar com o Google, a aplicação emite seu próprio token de sessão (ver skill `jwt-auth`) em vez de reusar o `id_token` do Google como sessão da aplicação.
