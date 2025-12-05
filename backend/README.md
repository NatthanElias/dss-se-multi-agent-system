# CEMA Backend - Multi-Agent System

CEMA system backend implemented with Google ADK, containing the multi-agent architecture and strategic analysis logic.

## 🏗️ Architecture
<div align="center">
  <img src="../static/tcc_DIAGRAMA_FinalBoss.drawio.png" alt="System diagram" width="500">
</div>

```
SequentialAgent (root)
    └── ParallelAgent (council)
            ├── CSO Agent (social impact)
            ├── CMO Agent (market + google\_search)
            ├── CFO Agent (finance + python\_repl)
            └── CRO Agent (risk + SWOT)
    └── CEO Agent (final synthesis)
```

## 🚀 Local Setup

### 1. Install dependencies

**With uv (recommended):**
```bash
cd backend
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
````

**With pip:**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2\. Configure API Key

1.  Go to https://aistudio.google.com/apikey
2.  Create an API key
3.  Copy `.env.example` to `.env`:

<!-- end list -->

```bash
cp .env.example .env
```

4.  Add your key to `.env`:

<!-- end list -->

```
GOOGLE_API_KEY=your_key_here
```

### 3\. Run the system

**CLI Mode:**

```bash
cd cema_system
adk run .
```

**Web UI Mode:**

```bash
cd cema_system
adk web .
```

Access http://localhost:8000

## 🧪 Testing

Examples of strategic dilemmas:

```
Should I expand service from 800 to 1200 beneficiaries in 6 months?
This will require hiring 15 new educators and increasing the budget by 35%.
```

```
Is it worth investing R$ 500,000 in technology to automate processes?
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Models
config.model.ceo_model = "gemini-2.5-pro"        # CEO uses Pro
config.model.default_model = "gemini-2.5-flash"  # Others use Flash

# Parameters
config.model.temperature = 0.3
config.model.max_tokens = 8000

# Language
config.language.output_language = 'pt-BR'
```

## 🔧 Models Used

  - **Gemini 2.5 Flash:** CSO, CMO, CFO, CRO
  - **Gemini 2.5 Pro:** CEO

## 🐛 Troubleshooting

**API key not found**

  - Check `.env` for `GOOGLE_API_KEY`

**Timeout**

  - Increase in `config.py`: `config.agents.timeout = 180`

**Error 503**

  - API temporarily overloaded, please wait

## 📚 References

  - [Google ADK Docs](https://google.github.io/adk-docs/)
  - [Gemini API](https://ai.google.dev/api)
