# CEMA Frontend - Interface Web

Interface web do sistema CEMA desenvolvida com Streamlit.

## 🎨 Funcionalidades

- **📚 Página 1:** Visualização de documentos da base de conhecimento
- **💬 Página 2:** Chat com o sistema multi-agente
- **ℹ️ Página 3:** Informações do projeto


## 🚀 Setup Local

### 1. Instalar dependências
```bash
cd frontend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar Backend URL

Crie `.streamlit/secrets.toml`:
```toml
BACKEND_URL = "http://localhost:8000"
```

### 3. Rodar
```bash
streamlit run app.py
```

Acesse http://localhost:8501

**Obs:** Mude porta com `--server.port 8502`

## 🧪 Testando

1. **Página Documentos:** Selecione "PEQUENA" e navegue pelas abas
2. **Página Chat:** Escolha empresa e faça uma pergunta
3. **Aguarde:** 30-90 segundos para análise completa

## 🐛 Troubleshooting

**Connection refused**
- Verifique se backend está rodando
- Confirme `BACKEND_URL` em `secrets.toml`

**Timeout**
- Backend pode estar lento (cold start Railway: ~60s)
- Aumente timeout em `2_💬_Sistema_CEMA.py`

**Documentos não aparecem**
- Copie `knowledge_base/` do backend
```bash
cp -r ../backend/cema_system/knowledge_base ./
```

## 📚 Referências

- [Streamlit Docs](https://docs.streamlit.io/)
