from pathlib import Path
from google.adk.agents import Agent
from prompts.cro_prompt import get_prompt


def load_knowledge_base() -> str:
    """
    Load CRO knowledge base from SWOT Analysis.
    
    CRO Agent requires:
    - doc5_swot_analysis.md
    
    Returns:
        str: Formatted knowledge base for context injection
    """
    kb_path = Path(__file__).parent.parent / "knowledge_base" / "PEQUENA"
    
    try:
        doc5 = (kb_path / "doc5_swot_analysis.md").read_text(encoding='utf-8')
        
        return f"""
        KNOWLEDGE BASE - CRO
        {'='*60}

        SWOT ANALYSIS:
        {doc5}

        {'='*60}
        """
    except FileNotFoundError as e:
        return f"ERROR: Missing {e.filename}"
    except Exception as e:
        return f"ERROR: {str(e)}"


# Load knowledge base
knowledge_base = load_knowledge_base()

# Get prompt with KB injected
instruction = get_prompt(knowledge_base)

cro_agent = Agent(
    model="gemini-2.5-flash",
    name="cro_agent",
    description="Chief Risk Officer - analyzes strategic risks using SWOT",
    instruction=instruction,
    output_key="cro_analysis"
)
