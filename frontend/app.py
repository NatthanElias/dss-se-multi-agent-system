import streamlit as st

st.set_page_config(
    page_title="CEMA - Sistema Multi-Agente",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("CEMA - Conselho Executivo Multi-Agente")
st.markdown("### *Sistema de Apoio à Decisão Estratégica*")
st.markdown("---")

st.markdown("""
## 👋 Bem-vindo!

Este é um **sistema de apoio à decisão estratégica** baseado em **Inteligência Artificial Multi-Agente**.

O CEMA simula um conselho executivo composto por 5 especialistas:
- 👥 **CSO** - Chief Social Officer (Impacto Social)
- 📊 **CMO** - Chief Marketing Officer (Mercado e Competição)  
- 💰 **CFO** - Chief Financial Officer (Viabilidade Financeira)
- ⚖️ **CRO** - Chief Risk Officer (Análise de Riscos)
- 🎯 **CEO** - Chief Executive Officer (Decisão Final)

---

## 📋 Tutorial - Como Funciona

### **Etapa 1: 📚 Conhecer os Documentos**
Visualize documentos reais de duas empresas de consultoria ESG:
- **PEQUENA** - Empresa de pequeno porte
- **MICROEMPRESA** - Empresa de micro porte

Após revisar, avalie a qualidade dos documentos.

### **Etapa 2: 💬 Interagir com o Sistema CEMA**
- Escolha o tipo de empresa
- Faça perguntas estratégicas ao sistema
- Veja análises de todos os 5 agentes especialistas
- Receba uma recomendação executiva final

### **Etapa 3: 📊 Avaliar o Sistema**
Dê seu feedback sobre a experiência.

---

## 🚀 Comece Agora!

Use o menu lateral para navegar pelas etapas do tutorial.
""")

with st.sidebar:
    st.markdown("### 📖 Navegação")
    st.info("""
**Etapas do Tutorial:**

1. 📚 **Documentos** - Visualize a base de conhecimento
2. 💬 **Sistema CEMA** - Interaja com os agentes
3. ℹ️ **Sobre** - Informações do projeto
    """)
    
    st.markdown("---")
    st.caption("💡 **Dica:** Siga as etapas em ordem para melhor experiência")
