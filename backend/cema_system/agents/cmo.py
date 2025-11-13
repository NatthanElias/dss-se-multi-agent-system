from google.adk.agents import Agent
from google.adk.tools import AgentTool
from google.adk.tools import google_search
from pathlib import Path
from ..prompts.cmo_prompt import get_prompt

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

# 1. Load Static Knowledge
knowledge_base = load_knowledge_base()

# 2. Get Prompt
prompt = get_prompt(knowledge_base)

# 3. Instantiate Agent with Tools
cmo_agent = Agent(
    model="gemini-2.5-flash",
    name="cmo_agent",
    description="Chief Marketing Officer - analyzes market and competition using Search",
    instruction=prompt,
    tools=[google_search],
    output_key="cmo_analysis"
)

# Wrap as Tool for the Coordinator
# cmo_tool = AgentTool(cmo_agent)
