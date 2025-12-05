# CEMA Frontend - Web Interface

CEMA system web interface developed with Streamlit.

## 🎨 Features

- **ℹ️ Page 1:** Project information
- **📚 Page 2:** Visualization of knowledge base documents
- **💬 Page 3:** Chat with the multi-agent system

## 🚀 Local Setup

### 1. Install dependencies
```bash
cd frontend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
````

### 2\. Configure Backend URL

Create `.streamlit/secrets.toml`:

```toml
BACKEND_URL = "http://localhost:8000"
```

### 3\. Run

```bash
streamlit run app.py
```

Access http://localhost:8501

**Note:** Change port with `--server.port 8502`

## 🧪 Testing

1.  **Documents Page:** Select "PEQUENA" or "MICROEMPRESA" and navigate through the tabs
2.  **Chat Page:** Ask a question with PEQUENA as base
3.  **Wait:** 30-90 seconds for complete analysis

## 🐛 Troubleshooting

**Connection refused**

  - Check if backend is running
  - Confirm `BACKEND_URL` in `secrets.toml`

**Timeout**

  - Backend might be slow (Railway cold start: \~60s)
  - Increase timeout in `2_💬_Sistema_CEMA.py`

**Documents not appearing**

  - Copy `knowledge_base/` from backend


```bash
cp -r ../backend/cema_system/knowledge_base ./
```

## 📚 References

  - [Streamlit Docs](https://docs.streamlit.io/)
