from google.adk.agents import Agent
from prompts.ceo_prompt import get_prompt

instruction = get_prompt()

ceo_agent = Agent(
    model="gemini-2.5-flash",
    name="ceo_agent",
    description="CEO - Final decision maker who synthesizes council analyses",
    instruction=instruction
)
