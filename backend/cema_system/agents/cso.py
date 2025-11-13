from google.adk.agents import Agent
from google.genai import types
from pathlib import Path
from ..prompts.cso_prompt import get_prompt
from ..config import config, get_model_for_agent


def load_knowledge_base() -> str:
    """
    Load social impact documents from knowledge base.
    
    CSO Agent requires:
    - doc1_mission_vision_values.md (Mission, Vision, Values)
    - doc3_social_impact_report.md (Social Impact Report)
    
    Returns:
        str: Formatted knowledge base for context injection
    """
    kb_path = Path(__file__).parent.parent / "knowledge_base" / "PEQUENA"
    
    try:
        # Load Mission, Vision & Values
        doc1_path = kb_path / "doc1_mission_vision_values.md"
        mission_vision_values = doc1_path.read_text(encoding='utf-8')
        
        # Load Social Impact Report
        doc3_path = kb_path / "doc3_social_impact_report.md"
        social_impact_report = doc3_path.read_text(encoding='utf-8')
        
        # Format knowledge base
        knowledge_base = f"""{'='*60}
        KNOWLEDGE BASE - CSO
        {'='*60}

        MISSION, VISION & VALUES:
        {mission_vision_values}

        ---

        SOCIAL IMPACT REPORT:
        {social_impact_report}

        {'='*60}
        """
        
        return knowledge_base
        
    except FileNotFoundError as e:
        return f"ERROR: Missing {e.filename}"
    except Exception as e:
        return f"ERRO ao carregar knowledge base: {str(e)}"


# Load knowledge base
knowledge_base = load_knowledge_base()

# Get prompt with language instruction
instruction = get_prompt(knowledge_base) + f"\n\n{config.language.language_instruction}"

cso_agent = Agent(
    model=get_model_for_agent("cso"),
    name="cso_agent",
    description="Chief Social Officer - analyzes social impact",
    instruction=instruction,
    output_key="cso_analysis",
    generate_content_config=types.GenerateContentConfig(
        temperature=config.model.temperature,
        max_output_tokens=config.model.max_tokens,
        top_p=config.model.top_p,
        top_k=config.model.top_k
    )
)
