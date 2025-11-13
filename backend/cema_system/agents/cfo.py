from google.adk.agents import Agent
from ..prompts.cfo_prompt import get_prompt
from ..tools.financial_repl import financial_python_repl
from ..config import config, get_model_for_agent
from google.genai import types


# Get prompt with language instruction
instruction = get_prompt() + f"\n\n{config.language.language_instruction}"

cfo_agent = Agent(
    model=get_model_for_agent("cfo"),
    name="cfo_agent",
    description="CFO - Financial Analyst with Python access",
    instruction=instruction,
    tools=[financial_python_repl], 
    output_key="cfo_analysis",
    generate_content_config=types.GenerateContentConfig(
        temperature=config.model.temperature,
        max_output_tokens=config.model.max_tokens,
        top_p=config.model.top_p,
        top_k=config.model.top_k
    )
)
