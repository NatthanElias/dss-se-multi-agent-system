import streamlit as st
import requests
import json
import uuid

st.set_page_config(
    page_title="Sistema CEMA",
    page_icon="💬",
    layout="wide"
)

# Backend URL
BACKEND_URL = st.secrets.get("BACKEND_URL", "https://cemasystem-production.up.railway.app")

st.title("💬 Sistema CEMA - Análise Multi-Agente")
st.markdown("### *Etapa 2: Interagir com o Sistema*")
st.markdown("---")

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]
if "messages" not in st.session_state:
    st.session_state.messages = []
if "company_selected" not in st.session_state:
    st.session_state.company_selected = False

# Step 1: Company Selection
if not st.session_state.company_selected:
    st.markdown("## 🏢 Etapa 2.1: Selecione a Empresa")
    st.info("Escolha qual empresa você deseja usar como contexto para as análises do CEMA")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏢 PEQUENA")
        st.caption("Empresa de pequeno porte")
        if st.button("Selecionar PEQUENA", use_container_width=True, type="primary"):
            st.session_state.company_type = "PEQUENA"
            st.session_state.company_selected = True
            st.rerun()
    
    with col2:
        st.markdown("### 🏪 MICROEMPRESA")
        st.caption("Empresa de micro porte")
        if st.button("Selecionar MICROEMPRESA", use_container_width=True, type="primary"):
            st.session_state.company_type = "MICROEMPRESA"
            st.session_state.company_selected = True
            st.rerun()
    
    st.markdown("---")
    st.warning("⚠️ Selecione uma empresa acima para continuar")
    st.stop()

# Display selected company
st.success(f"✅ **Empresa selecionada:** {st.session_state.company_type}")

# Suggested questions
with st.expander("💡 **Sugestões de Perguntas Estratégicas**", expanded=True):
    st.markdown("""
    **📈 Expansão e Crescimento:**
    - Devo expandir o atendimento de 800 para 1200 beneficiários em 6 meses?
    - Vale a pena abrir uma nova filial em outra cidade?
    - É viável contratar 15 novos consultores ESG?
    
    **💰 Investimentos:**
    - Devo investir R$ 500.000 em tecnologia para automatizar processos?
    - Vale a pena adquirir uma empresa concorrente menor?
    
    **🤝 Parcerias e Oportunidades:**
    - Devo aceitar uma parceria estratégica com grande empresa de tecnologia?
    - Vale a pena participar de edital governamental de R$ 2 milhões?
    - Devo firmar parceria com universidade para pesquisa em ESG?
    
    **🎯 Novos Produtos/Serviços:**
    - Devo lançar um novo serviço de consultoria em economia circular?
    - É o momento certo para criar um curso online sobre ESG?
    - Vale a pena desenvolver uma plataforma SaaS para gestão ESG?
    """)
    
    st.markdown("#### 🎯 Use estas perguntas como exemplo:")
    
    quick_questions = [
        "Devo expandir atendimento de 800 para 1200 beneficiários em 6 meses?",
        "Vale a pena investir R$ 500K em tecnologia?",
        "Devo aceitar parceria com grande empresa de tecnologia?"
    ]
    
    cols = st.columns(len(quick_questions))
    for idx, q in enumerate(quick_questions):
        with cols[idx]:
            if st.button(q, key=f"quick_{idx}", use_container_width=True):
                # Trigger chat with this question
                st.session_state.pending_question = q
                st.rerun()

# Process pending question
if "pending_question" in st.session_state:
    prompt = st.session_state.pending_question
    del st.session_state.pending_question
    
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("💬 Digite sua pergunta estratégica aqui..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Call CEMA backend
    with st.chat_message("assistant"):
        with st.spinner("🤖 **CEMA está analisando...**\n\n⏳ Executando análise multi-agente (CSO → CMO → CFO → CRO → CEO)"):
            try:
                # Prepare payload
                payload = {
                    "user_message": prompt,
                    "context": {
                        "company_type": st.session_state.company_type
                    }
                }
                
                # Call backend
                response = requests.post(
                    f"{BACKEND_URL}/run",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=180  # 3 minutes timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    assistant_message = result.get("output", "Erro: Resposta vazia")
                    
                    st.markdown(assistant_message)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_message
                    })
                else:
                    error_msg = f"❌ **Erro {response.status_code}**\n\n{response.text[:500]}"
                    st.error(error_msg)
                    
            except requests.exceptions.Timeout:
                st.error("⏱️ **Timeout:** O sistema demorou mais de 3 minutos. Tente uma pergunta mais simples.")
            except requests.exceptions.ConnectionError:
                st.error(f"🔌 **Erro de conexão:** Não foi possível conectar ao backend.\n\nURL: {BACKEND_URL}")
            except Exception as e:
                st.error(f"❌ **Erro inesperado:** {str(e)}")

st.markdown("---")

# Final evaluation
if len(st.session_state.messages) >= 2:
    st.markdown("## 📊 Avalie o Sistema CEMA")
    st.info("""
    Você já interagiu com o sistema! Por favor, avalie:
    - Qualidade das análises dos agentes
    - Utilidade da recomendação final
    - Experiência geral de uso
    """)
    
    form_url_2 = "https://forms.gle/SEU_LINK_FORMULARIO_2"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.link_button(
            "📋 Preencher Formulário de Avaliação do Sistema",
            form_url_2,
            use_container_width=True
        )

# Debug info (collapsible)
with st.expander("🔧 Informações de Debug"):
    st.json({
        "backend_url": BACKEND_URL,
        "session_id": st.session_state.session_id,
        "user_id": st.session_state.user_id,
        "company": st.session_state.get("company_type", "Not selected"),
        "messages_count": len(st.session_state.messages)
    })
