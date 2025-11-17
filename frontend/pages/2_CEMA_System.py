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

st.title("Sistema CEMA - Análise Multi-Agente")
st.markdown("### Etapa 2: Interagir com o Sistema")
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
        st.error(f"Erro ao criar sessão: {str(e)}")
        return False


def call_cema(prompt: str, company_type: str):
    """Call CEMA backend with proper ADK format"""
    
    # Create session if not exists
    if not st.session_state.session_created:
        with st.spinner("Inicializando sessão..."):
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
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/run",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=180
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erro {response.status_code}: {response.text[:500]}")
            return None
            
    except requests.exceptions.Timeout:
        st.error("Timeout: A análise demorou mais de 3 minutos. Tente novamente.")
        return None
    except Exception as e:
        st.error(f"Erro: {str(e)}")
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
    st.markdown("## Etapa 2.1: Selecione a Empresa")
    st.info("Escolha qual empresa você deseja usar como contexto para as análises do CEMA")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### PEQUENA")
        st.caption("Empresa de pequeno porte")
        if st.button("Selecionar PEQUENA", use_container_width=True, type="primary"):
            st.session_state.company_type = "PEQUENA"
            st.session_state.company_selected = True
            st.rerun()
    
    with col2:
        st.markdown("### MICROEMPRESA")
        st.caption("Empresa de micro porte")
        if st.button("Selecionar MICROEMPRESA", use_container_width=True, type="primary"):
            st.session_state.company_type = "MICROEMPRESA"
            st.session_state.company_selected = True
            st.rerun()
    
    st.markdown("---")
    st.warning("Selecione uma empresa acima para continuar")
    st.stop()

# Display selected company
st.success(f"Empresa selecionada: **{st.session_state.company_type}**")

# Suggested questions - ESG CONSULTING SPECIFIC
with st.expander("Sugestões de Perguntas Estratégicas", expanded=True):
    st.markdown("""
    ### Expansão e Crescimento
    - Devo expandir o atendimento de 800 para 1200 beneficiários em 6 meses, contratando 15 educadores e aumentando orçamento em 35%?
    - Vale a pena abrir uma filial em outra região do Brasil para atender novos mercados?
    - É viável dobrar a equipe de consultores ESG nos próximos 12 meses?
    
    ### Investimentos e Tecnologia
    - Devo investir R$ 500.000 em uma plataforma SaaS para gestão de relatórios ESG?
    - Vale a pena desenvolver um software próprio de monitoramento de métricas de sustentabilidade?
    - É o momento de contratar um CTO e formar equipe de tecnologia?
    
    ### Parcerias e Alianças
    - Devo aceitar parceria estratégica com grande consultoria internacional?
    - Vale a pena firmar aliança com universidade para pesquisa em economia circular?
    - É interessante criar joint-venture com startup de tecnologia climática?
    
    ### Novos Produtos e Serviços
    - Devo lançar serviço de certificação ESG própria?
    - Vale a pena criar programa de capacitação online em sustentabilidade corporativa?
    - É viável oferecer consultoria em créditos de carbono e mercado regulado?
    
    ### Mercado e Posicionamento
    - Devo focar exclusivamente em PMEs ou expandir para grandes empresas?
    - Vale a pena especializar-se em um setor específico (ex: agronegócio sustentável)?
    - É estratégico participar de edital governamental de R$ 2 milhões para capacitação ESG?
    """)
    
    st.markdown("---")
    st.markdown("#### Clique para usar uma pergunta de exemplo:")
    
    # ESG-specific quick questions
    quick_questions = [
        "Devo expandir atendimento de 800 para 1200 beneficiários em 6 meses, contratando 15 educadores e aumentando orçamento em 35%?",
        "Vale a pena investir R$ 500.000 em plataforma SaaS para gestão de relatórios ESG?",
        "Devo aceitar parceria estratégica com grande consultoria internacional de sustentabilidade?"
    ]
    
    # Create buttons in columns
    for idx, q in enumerate(quick_questions):
        if st.button(q, key=f"quick_{idx}", use_container_width=True):
            # Add to messages and trigger processing
            st.session_state.messages.append({"role": "user", "content": q})
            
            # Add user message display
            with st.chat_message("user"):
                st.markdown(q)
            
            # Call CEMA
            with st.chat_message("assistant"):
                status = st.status("CEMA está analisando...", expanded=True)
                
                status.write("Iniciando análise multi-agente...")
                status.write("CSO analisando impacto social...")
                status.write("CMO pesquisando mercado...")
                status.write("CFO calculando viabilidade financeira...")
                status.write("CRO avaliando riscos...")
                
                start_time = time.time()
                events = call_cema(q, st.session_state.company_type)
                elapsed = time.time() - start_time
                
                if events:
                    status.write("CEO sintetizando recomendação...")
                    status.update(label=f"Análise completa ({elapsed:.1f}s)", state="complete")
                    
                    # Parse response
                    analyses = parse_cema_response(events)
                    
                    if analyses["ceo_decision"]:
                        # Show expandable individual analyses
                        with st.expander("Ver Análises Individuais dos Agentes", expanded=False):
                            tab1, tab2, tab3, tab4 = st.tabs(["CSO", "CMO", "CFO", "CRO"])
                            
                            with tab1:
                                st.markdown(analyses.get("cso_analysis", "Análise não disponível"))
                            with tab2:
                                st.markdown(analyses.get("cmo_analysis", "Análise não disponível"))
                            with tab3:
                                st.markdown(analyses.get("cfo_analysis", "Análise não disponível"))
                            with tab4:
                                st.markdown(analyses.get("cro_analysis", "Análise não disponível"))
                        
                        # Show CEO decision
                        st.markdown("### Decisão Executiva (CEO)")
                        st.markdown(analyses["ceo_decision"])
                        
                        # Save to history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": analyses["ceo_decision"],
                            "analyses": analyses
                        })
                    else:
                        st.error("Não foi possível extrair a decisão do CEO")
                else:
                    status.update(label="Falha na análise", state="error")
            
            st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and "analyses" in message:
            # Show expandable analyses
            with st.expander("Ver Análises Individuais dos Agentes", expanded=False):
                tab1, tab2, tab3, tab4 = st.tabs(["CSO", "CMO", "CFO", "CRO"])
                
                with tab1:
                    st.markdown(message["analyses"].get("cso_analysis", "Não disponível"))
                with tab2:
                    st.markdown(message["analyses"].get("cmo_analysis", "Não disponível"))
                with tab3:
                    st.markdown(message["analyses"].get("cfo_analysis", "Não disponível"))
                with tab4:
                    st.markdown(message["analyses"].get("cro_analysis", "Não disponível"))
            
            # Show CEO decision
            st.markdown("### Decisão Executiva (CEO)")
            st.markdown(message["content"])
        else:
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Digite sua pergunta estratégica aqui..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Call CEMA
    with st.chat_message("assistant"):
        status = st.status("CEMA está analisando...", expanded=True)
        
        status.write("Iniciando análise multi-agente...")
        status.write("CSO analisando impacto social...")
        status.write("CMO pesquisando mercado...")
        status.write("CFO calculando viabilidade financeira...")
        status.write("CRO avaliando riscos...")
        
        start_time = time.time()
        events = call_cema(prompt, st.session_state.company_type)
        elapsed = time.time() - start_time
        
        if events:
            status.write("CEO sintetizando recomendação...")
            status.update(label=f"Análise completa ({elapsed:.1f}s)", state="complete")
            
            # Parse response
            analyses = parse_cema_response(events)
            
            if analyses["ceo_decision"]:
                # Show expandable individual analyses
                with st.expander("Ver Análises Individuais dos Agentes", expanded=False):
                    tab1, tab2, tab3, tab4 = st.tabs(["CSO", "CMO", "CFO", "CRO"])
                    
                    with tab1:
                        st.markdown(analyses.get("cso_analysis", "Análise não disponível"))
                    with tab2:
                        st.markdown(analyses.get("cmo_analysis", "Análise não disponível"))
                    with tab3:
                        st.markdown(analyses.get("cfo_analysis", "Análise não disponível"))
                    with tab4:
                        st.markdown(analyses.get("cro_analysis", "Análise não disponível"))
                
                # Show CEO decision
                st.markdown("### Decisão Executiva (CEO)")
                st.markdown(analyses["ceo_decision"])
                
                # Save to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": analyses["ceo_decision"],
                    "analyses": analyses
                })
            else:
                st.error("Não foi possível extrair a decisão do CEO")
        else:
            status.update(label="Falha na análise", state="error")

st.markdown("---")

# Final evaluation
if len(st.session_state.messages) >= 2:
    st.markdown("## Avalie o Sistema CEMA")
    st.info("""
    Você já interagiu com o sistema! Por favor, avalie:
    - Qualidade das análises dos agentes
    - Utilidade da recomendação final
    - Experiência geral de uso
    """)
    
    form_url_2 = "https://forms.gle/PxSZ8u6bi2dPRGWL7"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.link_button(
            "Preencher Formulário de Avaliação",
            form_url_2,
            use_container_width=True,
            type="primary"
        )
