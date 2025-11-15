import streamlit as st
import requests
import json
import uuid
import time

st.set_page_config(
    page_title="Sistema CEMA",
    page_icon="💬",
    layout="wide"
)

# Backend URL
BACKEND_URL = st.secrets.get("BACKEND_URL", "http://localhost:8000")

st.title("💬 Sistema CEMA - Análise Multi-Agente")
st.markdown("### *Etapa 2: Interagir com o Sistema*")
st.markdown("---")

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = f"session_{uuid.uuid4().hex[:12]}"
if "user_id" not in st.session_state:
    st.session_state.user_id = f"user_{uuid.uuid4().hex[:8]}"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "company_selected" not in st.session_state:
    st.session_state.company_selected = False
if "session_created" not in st.session_state:
    st.session_state.session_created = False


def create_session():
    """Create ADK session in backend"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/apps/cema_system/users/{st.session_state.user_id}/sessions/{st.session_state.session_id}",
            json={},
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        st.error(f"❌ Erro ao criar sessão: {str(e)}")
        return False


def call_cema(prompt: str, company_type: str):
    """Call CEMA backend with proper ADK format"""
    
    # Create session if not exists
    if not st.session_state.session_created:
        with st.spinner("🔧 Inicializando sessão..."):
            if create_session():
                st.session_state.session_created = True
            else:
                st.error("Falha ao criar sessão. Tente novamente.")
                return None
    
    # Build message with company context
    full_message = f"CONTEXTO: Empresa {company_type}.\n\nPERGUNTA: {prompt}"
    
    # ADK-compliant payload
    payload = {
        "app_name": "cema_system",
        "user_id": st.session_state.user_id,
        "session_id": st.session_state.session_id,
        "new_message": {
            "role": "user",
            "parts": [
                {
                    "text": full_message
                }
            ]
        }
    }

    # ============================================================================
    # DEBUG: Show what we're sending
    # ============================================================================
    with st.expander("🔧 DEBUG - Request Info", expanded=False):
        st.json({
            "backend_url": BACKEND_URL,
            "endpoint": f"{BACKEND_URL}/run",
            "payload": payload
        })
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/run",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=180
        )

        # ============================================================================
        # DEBUG: Show response
        # ============================================================================
        with st.expander("🔧 DEBUG - Response Info", expanded=False):
            st.code(f"Status: {response.status_code}")
            st.code(f"Response length: {len(response.text)} chars")
            if response.status_code != 200:
                st.code(response.text)
        # ============================================================================
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"❌ Erro {response.status_code}: {response.text[:500]}")
            return None
            
    except requests.exceptions.Timeout:
        st.error("⏱️ **Timeout:** A análise demorou mais de 3 minutos. Tente novamente.")
        return None
    except Exception as e:
        st.error(f"❌ Erro: {str(e)}")
        return None


def parse_cema_response(events_array):
    """Parse ADK events array and extract agent analyses"""
    
    analyses = {
        "cso_analysis": None,
        "cmo_analysis": None,
        "cfo_analysis": None,
        "cro_analysis": None,
        "ceo_decision": None
    }
    
    if not events_array or not isinstance(events_array, list):
        return analyses
    
    # Find last event with text content (CEO decision)
    for event in reversed(events_array):
        if "content" in event and "parts" in event["content"]:
            parts = event["content"]["parts"]
            if parts and "text" in parts[0]:
                analyses["ceo_decision"] = parts[0]["text"]
                break
    
    # Extract individual analyses from stateDelta
    for event in events_array:
        if "actions" in event and "stateDelta" in event["actions"]:
            state = event["actions"]["stateDelta"]
            
            if "cso_analysis" in state:
                analyses["cso_analysis"] = state["cso_analysis"]
            if "cmo_analysis" in state:
                analyses["cmo_analysis"] = state["cmo_analysis"]
            if "cfo_analysis" in state:
                analyses["cfo_analysis"] = state["cfo_analysis"]
            if "cro_analysis" in state:
                analyses["cro_analysis"] = state["cro_analysis"]
    
    return analyses


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
    
    st.markdown("#### 🎯 Clique para usar uma pergunta:")
    
    quick_questions = [
        "Devo expandir atendimento de 800 para 1200 beneficiários em 6 meses, contratando 15 educadores e aumentando orçamento em 35%?",
        "Vale a pena investir R$ 500K em tecnologia?",
        "Devo aceitar parceria com grande empresa de tecnologia?"
    ]
    
    cols = st.columns(len(quick_questions))
    for idx, q in enumerate(quick_questions):
        with cols[idx]:
            if st.button(f"❓ {q[:40]}...", key=f"quick_{idx}", use_container_width=True):
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
        if message["role"] == "assistant" and "analyses" in message:
            # Show expandable analyses
            with st.expander("📊 Ver Análises Individuais dos Agentes"):
                tab1, tab2, tab3, tab4 = st.tabs(["👥 CSO", "📊 CMO", "💰 CFO", "⚖️ CRO"])
                
                with tab1:
                    st.markdown(message["analyses"].get("cso_analysis", "Não disponível"))
                with tab2:
                    st.markdown(message["analyses"].get("cmo_analysis", "Não disponível"))
                with tab3:
                    st.markdown(message["analyses"].get("cfo_analysis", "Não disponível"))
                with tab4:
                    st.markdown(message["analyses"].get("cro_analysis", "Não disponível"))
            
            # Show CEO decision
            st.markdown("### 🎯 Decisão Executiva (CEO)")
            st.markdown(message["content"])
        else:
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("💬 Digite sua pergunta estratégica aqui..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Call CEMA
    with st.chat_message("assistant"):
        status = st.status("🤖 CEMA está analisando...", expanded=True)
        
        status.write("⏳ Iniciando análise multi-agente...")
        status.write("👥 CSO analisando impacto social...")
        status.write("📊 CMO pesquisando mercado...")
        status.write("💰 CFO calculando viabilidade financeira...")
        status.write("⚖️ CRO avaliando riscos...")
        
        start_time = time.time()
        events = call_cema(prompt, st.session_state.company_type)
        elapsed = time.time() - start_time
        
        if events:
            status.write("🎯 CEO sintetizando recomendação...")
            status.update(label=f"✅ Análise completa! ({elapsed:.1f}s)", state="complete")
            
            # Parse response
            analyses = parse_cema_response(events)
            
            if analyses["ceo_decision"]:
                # Show expandable individual analyses
                with st.expander("📊 Ver Análises Individuais dos Agentes", expanded=False):
                    tab1, tab2, tab3, tab4 = st.tabs(["👥 CSO", "📊 CMO", "💰 CFO", "⚖️ CRO"])
                    
                    with tab1:
                        st.markdown(analyses.get("cso_analysis", "❌ Análise não disponível"))
                    with tab2:
                        st.markdown(analyses.get("cmo_analysis", "❌ Análise não disponível"))
                    with tab3:
                        st.markdown(analyses.get("cfo_analysis", "❌ Análise não disponível"))
                    with tab4:
                        st.markdown(analyses.get("cro_analysis", "❌ Análise não disponível"))
                
                # Show CEO decision
                st.markdown("### 🎯 Decisão Executiva (CEO)")
                st.markdown(analyses["ceo_decision"])
                
                # Save to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": analyses["ceo_decision"],
                    "analyses": analyses
                })
            else:
                st.error("❌ Não foi possível extrair a decisão do CEO")
        else:
            status.update(label="❌ Falha na análise", state="error")

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

# Debug info
with st.expander("🔧 Informações de Debug"):
    st.json({
        "backend_url": BACKEND_URL,
        "session_id": st.session_state.session_id,
        "user_id": st.session_state.user_id,
        "session_created": st.session_state.session_created,
        "company": st.session_state.get("company_type", "Not selected"),
        "messages_count": len(st.session_state.messages)
    })
