# API CEMA Backend

API simplificada para o Sistema Multiagente CEMA.

## Visão Geral

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/health` | GET | Verificar status da API |
| `/apps/{appName}/users/{userId}/sessions/{sessionId}` | POST | Criar sessão |
| `/apps/{appName}/users/{userId}/sessions/{sessionId}` | GET | Obter sessão |
| `/run` | POST | Executar agente |

---

## 1. Health Check

Verifica se a API está funcionando.

**Requisição:**
```bash
GET /health
```

**Resposta:**
```json
{
  "status": "healthy",
  "service": "cema-backend"
}
```

---

## 2. Criar Sessão

Cria uma nova sessão para conversar com o agente. **Obrigatório antes de usar `/run`**.

**Requisição:**
```bash
POST /apps/{appName}/users/{userId}/sessions/{sessionId}
Content-Type: application/json

{
  "contexto": "opcional"
}
```

**Parâmetros:**
- `appName`: Nome da aplicação (ex: `cema_system`)
- `userId`: ID do usuário (ex: `user_123`)
- `sessionId`: ID da sessão (ex: `session_456`)

**Exemplo:**
```bash
curl -X POST "http://localhost:8000/apps/cema_system/users/user_123/sessions/session_456" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Resposta:**
```json
{
  "id": "session_456",
  "appName": "cema_system",
  "userId": "user_123",
  "state": {},
  "events": [],
  "lastUpdateTime": "2025-12-15T22:00:00"
}
```

---

## 3. Executar Agente

Envia uma mensagem para o agente e recebe a resposta.

**Requisição:**
```bash
POST /run
Content-Type: application/json

{
  "appName": "cema_system",
  "userId": "user_123",
  "sessionId": "session_456",
  "newMessage": {
    "role": "user",
    "parts": [{"text": "Sua pergunta aqui"}]
  }
}
```

**Campos obrigatórios:**
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `appName` | string | Nome da aplicação |
| `userId` | string | ID do usuário |
| `sessionId` | string | ID da sessão (já criada) |
| `newMessage.role` | string | `"user"` ou `"model"` |
| `newMessage.parts` | array | Lista com objetos `{text: "..."}` |

**Exemplo:**
```bash
curl -X POST "http://localhost:8000/run" \
  -H "Content-Type: application/json" \
  -d '{
    "appName": "cema_system",
    "userId": "user_123",
    "sessionId": "session_456",
    "newMessage": {
      "role": "user",
      "parts": [{"text": "Analise as tendências do setor de tecnologia"}]
    }
  }'
```

**Resposta:**
```json
[
  {
    "author": "cso_agent",
    "invocationId": "abc123",
    "content": {
      "role": "model",
      "parts": [{"text": "Análise estratégica do CSO..."}]
    }
  },
  {
    "author": "ceo_agent",
    "invocationId": "xyz789",
    "content": {
      "role": "model",
      "parts": [{"text": "Síntese final do CEO..."}]
    }
  }
]
```

---

## 4. Obter Sessão

Recupera os dados de uma sessão existente.

**Requisição:**
```bash
GET /apps/{appName}/users/{userId}/sessions/{sessionId}
```

**Exemplo:**
```bash
curl "http://localhost:8000/apps/cema_system/users/user_123/sessions/session_456"
```

---

## 5. Listar Aplicações

Lista as aplicações disponíveis.

**Requisição:**
```bash
GET /list-apps
```

**Resposta:**
```json
{
  "apps": ["cema_system"]
}
```

---

## Fluxo de Uso

```
1. Iniciar servidor    → python server.py
2. Criar sessão        → POST /apps/.../sessions/...
3. Executar agente     → POST /run
4. (Opcional) Repetir execuções na mesma sessão
```

---

## Documentação Interativa

Acesse `/docs` para ver a documentação Swagger UI:
```
http://localhost:8000/docs
```
