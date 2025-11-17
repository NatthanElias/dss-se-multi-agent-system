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


def call_cema(prompt: str):
    """Call CEMA backend with proper ADK format"""
    
    # Create session if not exists
    if not st.session_state.session_created:
        with st.spinner("Inicializando sessão..."):
            if create_session():
                st.session_state.session_created = True
            else:
                st.error("Falha ao criar sessão. Tente novamente.")
                return None
    
    # ADK-compliant payload
    payload = {
        "app_name": "cema_system",
        "user_id": st.session_state.user_id,
        "session_id": st.session_state.session_id,
        "new_message": {
            "role": "user",
            "parts": [
                {
                    "text": prompt
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


# Display company info (fixed)
st.info(f"📊 **Contexto da Análise:** Empresa de Pequeno Porte (PEQUENA)")

# Suggested questions - ESG CONSULTING SPECIFIC
with st.expander("💡 Sugestões de Perguntas Estratégicas", expanded=False):
    st.markdown("""
    ### 📈 Expansão e Crescimento
    - Devo expandir de 25 para 40 clientes nos próximos 12 meses, contratando 8 novos consultores?
    - Vale a pena abrir um escritório comercial em São Paulo para prospecção no Sudeste?
    - É viável aumentar a equipe de 41 para 55 funcionários até o final de 2026?
    
    ### 💰 Investimentos e Tecnologia
    - Devo investir R$ 150.000 em CRM e ferramenta de gestão de projetos ESG?
    - Vale a pena desenvolver uma calculadora online de pegada de carbono para PMEs?
    - É o momento de contratar um especialista em tecnologia climática?
    
    ### 🤝 Parcerias e Alianças
    - Devo firmar parceria com cooperativa de reciclagem para projetos de economia circular?
    - Vale a pena criar aliança com incubadora de startups sustentáveis?
    - É interessante associar-me à rede B-Corp para aumentar credibilidade?
    
    ### 🎯 Novos Produtos e Serviços
    - Devo lançar serviço de diagnóstico ESG rápido (R$ 5.000) para micro e pequenas empresas?
    - Vale a pena criar curso online de introdução à economia circular?
    - É viável oferecer consultoria em certificação de turismo sustentável?
    
    ### 🌱 Mercado e Posicionamento  
    - Devo especializar a empresa exclusivamente em economia circular e deixar outros serviços ESG?
    - Vale a pena focar apenas no setor de alimentos orgânicos e turismo sustentável?
    - É estratégico participar de edital SEBRAE de R$ 300.000 para capacitação em ESG?
    
    ### ♻️ Sustentabilidade e Impacto
    - Devo criar meta de reduzir 100 toneladas de CO2e através de projetos de clientes até 2026?
    - Vale a pena implementar programa de certificação própria em economia circular?
    - É viável criar laboratório de inovação em sustentabilidade com universidade local?
    """)
    
    st.markdown("---")
    st.markdown("#### ⚡ Clique para usar uma pergunta de exemplo:")
    
    # Realistic quick questions for PEQUENA company
    quick_questions = [
        "Devo expandir de 25 para 40 clientes nos próximos 12 meses, contratando 8 novos consultores?",
        "Vale a pena investir R$ 150.000 em CRM e ferramenta de gestão de projetos ESG?",
        "Devo especializar a empresa exclusivamente em economia circular e deixar outros serviços ESG?"
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
                events = call_cema(q)
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
        events = call_cema(prompt)
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
