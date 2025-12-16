# WALKTHROUGH - Teste Completo do Sistema de Microserviços

Guia passo-a-passo para testar toda a arquitetura de microserviços.

---

## Postman Collection

on `test/postman/CEMA_api_testing.postman_collection.json`

---

## 1. Iniciar os Serviços

Você precisará de **3 terminais** abertos simultaneamente.

### Terminal 1 - Auth Service (Porta 3001)

```bash
cd auth-service
npm start
```

**Output esperado:**
```
[Auth] Default admin user created
[Auth Service] Running on http://localhost:3001
[Auth Service] Endpoints:
  POST /auth/login    - Login with credentials
  GET  /auth/validate - Validate JWT token
  GET  /auth/health   - Health check
```

### Terminal 2 - Agent Service (Porta 8080)

```bash
python3 server.py
```

**Output esperado:**
```
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

### Terminal 3 - API Gateway (Porta 3000)

```bash
cd api-gateway
npm start
```

**Output esperado:**
```
==================================================
[API Gateway] Running on http://localhost:3000
==================================================

Routing Configuration:
  /auth/*  → http://localhost:3001
  /api/*   → http://localhost:8080
  /health  → Gateway health check

==================================================
```

---

## 2. Testar Health Checks

Verifique se todos os serviços estão respondendo.

### 2.1 Gateway Health

```bash
curl http://localhost:3000/health
```

**Resposta esperada:**
```json
{
  "status": "healthy",
  "service": "api-gateway",
  "routes": {
    "auth": "http://localhost:3001",
    "agent": "http://localhost:8080"
  }
}
```

### 2.2 Auth Service Health (via Gateway)

```bash
curl http://localhost:3000/auth/health
```

**Resposta esperada:**
```json
{"status":"healthy","service":"auth-service"}
```

### 2.3 Agent Service Health (via Gateway)

```bash
curl http://localhost:3000/api/health
```

**Resposta esperada:**
```json
{"status":"healthy","service":"agent-service"}
```

---

## 3. Testar Autenticação

### 3.1 Login com Usuário Padrão

```bash
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

**Resposta esperada:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

*IMPORTANTE:* Copie o valor do `access_token` para usar nos próximos passos!

### 3.2 Validar Token

Substitua `<TOKEN>` pelo token obtido no login:

```bash
curl http://localhost:3000/auth/validate \
  -H "Authorization: Bearer <TOKEN>"
```

**Resposta esperada:**
```json
{"valid":true,"user":"admin","exp":1702876800}
```

---

## 4. Testar Endpoints do Agente
  
### 4.1 Criar Sessão

Substitua `<TOKEN>` pelo token obtido:

```bash
curl -X POST "http://localhost:3000/api/apps/cema_system/users/user123/sessions/session001" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Resposta esperada:** Objeto de sessão com `id`, `appName`, `userId`, etc.

### 4.2 Executar Agente

```bash
curl -X POST http://localhost:3000/api/run \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "appName": "cema_system",
    "userId": "user123",
    "sessionId": "session001",
    "newMessage": {
      "role": "user",
      "parts": [{"text": "Devo expandir o atendimento de 800 para 1200 beneficiários?"}]
    }
  }'
```

**Resposta esperada:** Array de eventos com respostas dos agentes CSO, CMO, CFO, CRO e CEO.

---

## 5. Testar Tratamento de Erros

### 5.1 Rota Não Encontrada

```bash
curl http://localhost:3000/invalid/route
```

**Resposta esperada:**
```json
{
  "detail": "Route not found",
  "hint": "Use /auth/* for authentication or /api/* for agent operations"
}
```

### 5.2 Credenciais Inválidas

```bash
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"wrong","password":"wrong"}'
```

**Resposta esperada:**
```json
{"detail":"Incorrect username or password"}
```

### 5.3 Token Inválido

```bash
curl http://localhost:3000/auth/validate \
  -H "Authorization: Bearer invalid_token_here"
```

**Resposta esperada:**
```json
{"valid":false,"detail":"Invalid token"}
```

---

## 6. Verificar Logs

### Terminal do Gateway

Você deve ver logs como:
```
[2024-12-15T23:30:00.000Z] POST /auth/login → Routing...
[Gateway] Routing to Auth Service: /auth/login
[2024-12-15T23:30:05.000Z] POST /api/run → Routing...
[Gateway] Routing to Agent Service: /api/run
```

### Terminal do Auth Service

```
[Auth] User logged in: admin

```

---

## 7. Resumo da Arquitetura Testada

| Serviço | Porta | Endpoints Testados |
|---------|-------|-------------------|
| API Gateway | 3000 | `/health`, `/`, (routing) |
| Auth Service | 3001 | `/auth/login`, `/auth/validate`, `/auth/health` |
| Agent Service | 8080 | `/api/health`, `/api/apps/.../sessions/...`, `/api/run` |