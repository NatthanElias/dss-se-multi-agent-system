from google.adk.agents import Agent
from ..config import config, get_model_for_agent
from ..prompts.ceo_prompt import get_prompt
from google.genai import types


instruction = get_prompt() + f"\n\n{config.language.language_instruction}"

ceo_agent = Agent(
    model=get_model_for_agent("ceo"),
    name="ceo_agent",
    description="CEO - Final decision maker who synthesizes council analyses",
    instruction=instruction,
    generate_content_config=types.GenerateContentConfig(
        temperature=config.model.temperature,
        max_output_tokens=config.model.max_tokens,
        top_p=config.model.top_p,
        top_k=config.model.top_k
    )
)
