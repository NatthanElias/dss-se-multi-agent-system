from google.adk.agents import Agent
from google.genai import types
from google.adk.tools import google_search
from pathlib import Path
from ..prompts.cmo_prompt import get_prompt
from ..config import config, get_model_for_agent


def load_knowledge_base() -> str:
    """
    Load market-relevant documents from knowledge base.
    
    CMO Agent requires:
    - doc4_business_model_canvas.md
    
    Returns:
        str: Formatted knowledge base for context injection.
    """
    kb_path = Path(__file__).parent.parent / "knowledge_base" / "PEQUENA"
    
    try:
        # Load Business Model Canvas
        doc4_path = kb_path / "doc4_business_model_canvas.md"
        bmc_content = doc4_path.read_text(encoding='utf-8')
        
        # Format knowledge base
        knowledge_base = f"""{'='*60}
        KNOWLEDGE BASE - CMO
        {'='*60}

        BUSINESS MODEL CANVAS:
        {bmc_content}

        {'='*60}
        """
        
        return knowledge_base
        
    except FileNotFoundError as e:
        return f"ERROR: Missing {e.filename}"
    except Exception as e:
        return f"ERROR loading knowledge base: {str(e)}"

# Load Static Knowledge
knowledge_base = load_knowledge_base()

# Get prompt with language instruction
instruction = get_prompt(knowledge_base) + f"\n\n{config.language.language_instruction}"

# 3. Instantiate Agent with Tools
cmo_agent = Agent(
    model=get_model_for_agent("cmo"),
    name="cmo_agent",
    description="Chief Marketing Officer - analyzes market and competition using Search",
    instruction=instruction,
    tools=[google_search],
    output_key="cmo_analysis",
    generate_content_config=types.GenerateContentConfig(
        temperature=config.model.temperature,
        max_output_tokens=config.model.max_tokens,
        top_p=config.model.top_p,
        top_k=config.model.top_k
    )
)
