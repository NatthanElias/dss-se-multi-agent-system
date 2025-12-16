# API CEMA - Arquitetura de Microserviços

Sistema Multiagente CEMA implementado com arquitetura de microserviços e API Gateway.

## 🏗️ Arquitetura

```
┌──────────────────────────────────────────────────────────────┐
│                 Clientes (Postman/Browser)                   │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│              API Gateway (Node.js - Porta 3000)              │
│                                                              │
│  • Roteamento de requisições                                 │
│  • Logging centralizado                                      │
│  • Tratamento de erros                                       │
│  • Configuração CORS                                         │
└──────────────────┬─────────────────────────┬─────────────────┘
                   │                         │
              /auth/*                    /api/*
                   │                         │
                   ▼                         ▼
┌─────────────────────────────┐   ┌────────────────────────────┐
│   Auth Service (Node.js)    │   │  Agent Service (Python)    │
│        Porta 3001           │   │       Porta 8080           │
├─────────────────────────────┤   ├────────────────────────────┤
│ POST /auth/login            │   │ POST /api/apps/.../sessions│
│ GET  /auth/validate         │   │ POST /api/run              │
│ PATCH/api/apps/.../sessions │   │ GET  /api/health           │
│                             │   │                            │
│ • JWT Authentication        │   │ • Google ADK Agent         │
│ • bcrypt Password Hashing   │   │ • Session Management       │
│ • IP Blacklist              │   │                            │
└─────────────────────────────┘   └────────────────────────────┘
```

---

## 📋 Visão Geral dos Endpoints

Todos os endpoints são acessados através do **API Gateway** na porta **3000**.

### Autenticação (Auth Service)

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/auth/login` | POST | Login com credenciais, retorna JWT |
| `/auth/validate` | GET | **[AUTH]** Validar token JWT |
| `/auth/health` | GET | Health check do Auth Service |

### Agente e Sessões (Agent Service)

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/apps/{appName}/users/{userId}/sessions/{sessionId}` | POST | **[AUTH]** Criar sessão |
| `/api/apps/{appName}/users/{userId}/sessions/{sessionId}` | GET | **[AUTH]** Obter sessão |
| `/api/run` | POST | **[AUTH]** Executar agente e receber eventos |
| `/api/health` | GET | Health check do Agent Service |

### Gateway

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/health` | GET | Health check do Gateway |
| `/` | GET | Informações do Gateway |

---

## 🔐 Autenticação e Segurança

### JWT (JSON Web Tokens)

1. Faça **Login** com usuário e senha
2. Receba um **Access Token** (expira em 24h)
3. Envie o token no **Header** das requisições protegidas

```
Authorization: Bearer <SEU_TOKEN_AQUI>
```

### Usuário Padrão

Para fins educacionais:
- **Username:** `admin`
- **Password:** `admin123`

### IP Blacklist

O arquivo `blacklist.txt` em cada serviço contém IPs banidos.
IPs na lista recebem erro `403 Forbidden`.

---

## 1. Login (Autenticação)

Obtém o token JWT necessário para usar os endpoints protegidos.

**Requisição:**
```bash
POST http://localhost:3000/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Exemplo cURL:**
```bash
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 2. Validar Token

Verifica se um token JWT é válido.

**Requisição:**
```bash
GET http://localhost:3000/auth/validate
Authorization: Bearer <SEU_TOKEN>
```

**Resposta:**
```json
{"valid": true, "user": "admin", "exp": 1702789200}
```

---

## 3. Health Checks

### Gateway
```bash
curl http://localhost:3000/health
```
```json
{"status": "healthy", "service": "api-gateway", "routes": {...}}
```

### Auth Service
```bash
curl http://localhost:3000/auth/health
```
```json
{"status": "healthy", "service": "auth-service"}
```

### Agent Service
```bash
curl http://localhost:3000/api/health
```
```json
{"status": "healthy", "service": "agent-service"}
```

---

## 4. Criar Sessão (Requer Token 🔒)

Cria uma nova sessão para conversar com o agente.

**Requisição:**
```bash
POST http://localhost:3000/api/apps/{appName}/users/{userId}/sessions/{sessionId}
Authorization: Bearer <SEU_TOKEN>
Content-Type: application/json

{}
```

**Exemplo:**
```bash
curl -X POST "http://localhost:3000/api/apps/cema_system/users/user_123/sessions/session_456" \
  -H "Authorization: Bearer <SEU_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

## 5. Executar Agente (Requer Token 🔒)

Envia uma mensagem para o agente e recebe a resposta.

**Requisição:**
```bash
POST http://localhost:3000/api/run
Authorization: Bearer <SEU_TOKEN>
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

**Exemplo:**
```bash
curl -X POST "http://localhost:3000/api/run" \
  -H "Authorization: Bearer <SEU_TOKEN>" \
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

**Resposta:** (Array de eventos)
```json
[
  {
    "author": "cso_agent",
    "content": { "role": "model", "parts": [{"text": "..."}] }
  }
]
```

---



---

## 📂 Estrutura do Projeto

```
backend/
├── api-gateway/          # Gateway Node.js (Porta 3000)
│   ├── server.js
│   ├── package.json
│   └── .env.example
│
├── auth-service/         # Auth Service Node.js (Porta 3001)
│   ├── server.js
│   ├── package.json
│   ├── blacklist.txt
│   └── .env.example
│
├── app/                  # Agent Service Python (Porta 8080)
│   ├── routes/
│   │   ├── agent.py
│   │   ├── session.py
│   │   ├── health.py
│   ├── services/
│   └── controllers/
│
├── server.py             # Entry point do Agent Service
├── requirements.txt
└── blacklist.txt
```

---

## ⚡ Quick Start

### Pré-requisitos
- Node.js 18+
- Python 3.10+
- npm

### Instalação

```bash
# 1. Auth Service
cd backend/auth-service
npm install

# 2. API Gateway
cd ../api-gateway
npm install

# 3. Agent Service
cd ..
pip install -r requirements.txt
```

### Executar (3 terminais)

**Terminal 1 - Auth Service:**
```bash
cd backend/auth-service
npm start
# [Auth Service] Running on http://localhost:3001
```

**Terminal 2 - Agent Service:**
```bash
cd backend
python server.py
# Uvicorn running on http://0.0.0.0:8080
```

**Terminal 3 - API Gateway:**
```bash
cd backend/api-gateway
npm start
# [API Gateway] Running on http://localhost:3000
```

---

## 🧪 Fluxo de Teste Completo

1. **Verificar serviços:**
   ```bash
   curl http://localhost:3000/health
   curl http://localhost:3000/auth/health
   curl http://localhost:3000/api/health
   ```

2. **Login:**
   ```bash
   curl -X POST http://localhost:3000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"admin123"}'
   ```

3. **Criar sessão:**
   ```bash
   curl -X POST "http://localhost:3000/api/apps/cema_system/users/user123/sessions/sess1" \
     -H "Authorization: Bearer <TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{}'
   ```

4. **Executar agente:**
   ```bash
   curl -X POST http://localhost:3000/api/run \
     -H "Authorization: Bearer <TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{
       "appName":"cema_system",
       "userId":"user123",
       "sessionId":"sess1",
       "newMessage":{"role":"user","parts":[{"text":"Hello"}]}
     }'
   ```

---

## 📖 Documentação Interativa

Acesse a documentação Swagger do Agent Service:
```
http://localhost:8080/docs
```

---

## 🛠️ Tecnologias

- **API Gateway:** Node.js + Express + express-http-proxy
- **Auth Service:** Node.js + Express + JWT + bcrypt
- **Agent Service:** Python + FastAPI + Google ADK

---

## Postman Collection

on `test/postman/CEMA_api_testing.postman_collection.json`