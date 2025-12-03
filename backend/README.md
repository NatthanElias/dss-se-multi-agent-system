# CEMA Backend - Sistema Multi-Agente

Backend do sistema CEMA implementado com Google ADK, contendo a arquitetura multi-agente e lógica de análise estratégica.

## 🏗️ Arquitetura
```
SequentialAgent (root)
    └── ParallelAgent (council)
            ├── CSO Agent (social impact)
            ├── CMO Agent (market + google_search)
            ├── CFO Agent (finance + python_repl)
            └── CRO Agent (risk + SWOT)
    └── CEO Agent (final synthesis)
```

## 🚀 Setup Local

### 1. Instalar dependências

**Com uv (recomendado):**
```bash
cd backend
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

**Com pip:**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurar API Key

1. Acesse https://aistudio.google.com/apikey
2. Crie uma API key
3. Copie `.env.example` para `.env`:
```bash
cp .env.example .env
```
4. Adicione sua chave no `.env`:
```
GOOGLE_API_KEY=sua_chave_aqui
```

### 3. Rodar o sistema

**Modo CLI:**
```bash
cd cema_system
adk run .
```

**Modo Web UI:**
```bash
cd cema_system
adk web .
```
Acesse http://localhost:8000

## 🧪 Testando

Exemplos de dilemas estratégicos:
```
Devo expandir atendimento de 800 para 1200 beneficiários em 6 meses?
Isso exigirá contratar 15 novos educadores e aumentar orçamento em 35%.
```
```
Vale a pena investir R$ 500.000 em tecnologia para automatizar processos?
```

## ⚙️ Configuração

Edite `config.py` para customizar:
```python
# Modelos
config.model.ceo_model = "gemini-2.5-pro"        # CEO usa Pro
config.model.default_model = "gemini-2.5-flash"  # Demais usam Flash

# Parâmetros
config.model.temperature = 0.3
config.model.max_tokens = 8000

# Idioma
config.language.output_language = 'pt-BR'
```

## 🔧 Modelos Usados

- **Gemini 2.5 Flash:** CSO, CMO, CFO, CRO
- **Gemini 2.5 Pro:** CEO

## 🐛 Troubleshooting

**API key not found**
- Verifique `.env` com `GOOGLE_API_KEY`

**Timeout**
- Aumente em `config.py`: `config.agents.timeout = 180`

**Erro 503**
- API temporariamente sobrecarregada, aguarde

## 📚 Referências

- [Google ADK Docs](https://google.github.io/adk-docs/)
- [Gemini API](https://ai.google.dev/api)
