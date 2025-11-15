import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Documentos - CEMA",
    page_icon="📚",
    layout="wide"
)

st.title("Base de Conhecimento - Documentos das Empresas")
st.markdown("### Etapa 1: Conhecer as Empresas")
st.markdown("---")

# Company selector
st.markdown("## Selecione a Empresa")
company_type = st.radio(
    "Escolha o tipo de empresa para visualizar os documentos:",
    ["PEQUENA", "MICROEMPRESA"],
    horizontal=True,
    help="Selecione entre empresa de pequeno ou micro porte"
)

st.info(f"Visualizando documentos da empresa: **{company_type}**")

# Get absolute path
current_dir = Path(__file__).parent.parent
kb_path = current_dir / "knowledge_base" / company_type

# Document tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Missão, Visão e Valores",
    "DRE (Demonstrativo)",
    "Impacto Social",
    "Business Model Canvas",
    "Análise SWOT"
])

# Tab 1: Mission
with tab1:
    st.markdown("### Missão, Visão e Valores")
    try:
        doc_path = kb_path / "doc1_mission_vision_values.md"
        doc = doc_path.read_text(encoding='utf-8')
        st.markdown(doc)
    except FileNotFoundError:
        st.error(f"Documento não encontrado: {doc_path}")
    except Exception as e:
        st.error(f"Erro ao ler documento: {str(e)}")

# Tab 2: DRE
with tab2:
    st.markdown("### Demonstrativo de Resultado do Exercício (DRE)")
    try:
        doc_path = kb_path / "doc2_dre.csv"
        df = pd.read_csv(doc_path)
        st.dataframe(df, use_container_width=True, height=400)
        
        col1, col2 = st.columns([3, 1])
        with col2:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Baixar CSV",
                csv,
                f"dre_{company_type.lower()}.csv",
                "text/csv",
                use_container_width=True
            )
    except FileNotFoundError:
        st.error(f"Documento não encontrado: {doc_path}")
    except Exception as e:
        st.error(f"Erro: {str(e)}")

# Tab 3: Social Impact
with tab3:
    st.markdown("### Relatório de Impacto Social")
    try:
        doc_path = kb_path / "doc3_social_impact_report.md"
        doc = doc_path.read_text(encoding='utf-8')
        st.markdown(doc)
    except FileNotFoundError:
        st.error(f"Documento não encontrado: {doc_path}")
    except Exception as e:
        st.error(f"Erro: {str(e)}")

# Tab 4: Canvas
with tab4:
    st.markdown("### Business Model Canvas")
    try:
        doc_path = kb_path / "doc4_business_model_canvas.md"
        doc = doc_path.read_text(encoding='utf-8')
        st.markdown(doc)
    except FileNotFoundError:
        st.error(f"Documento não encontrado: {doc_path}")
    except Exception as e:
        st.error(f"Erro: {str(e)}")

# Tab 5: SWOT
with tab5:
    st.markdown("### Análise SWOT")
    try:
        doc_path = kb_path / "doc5_swot_analysis.md"
        doc = doc_path.read_text(encoding='utf-8')
        st.markdown(doc)
    except FileNotFoundError:
        st.error(f"Documento não encontrado: {doc_path}")
    except Exception as e:
        st.error(f"Erro: {str(e)}")

st.markdown("---")

# Evaluation section
st.markdown("## Avalie a Qualidade dos Documentos")
st.info("""
Após revisar os documentos acima, por favor avalie:
- Clareza e completude das informações
- Realismo dos dados apresentados
- Utilidade para tomada de decisão estratégica
""")

form_url_1 = "https://forms.gle/SEU_LINK_FORMULARIO_1"

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.link_button(
        "Preencher Formulário de Avaliação",
        form_url_1,
        use_container_width=True,
        type="primary"
    )

st.success("Após preencher o formulário, prossiga para a próxima página: **Sistema CEMA**")
