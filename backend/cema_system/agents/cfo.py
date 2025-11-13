from google.adk.agents import Agent
from google.adk.tools import AgentTool
from ..prompts.cfo_prompt import get_prompt
from ..tools.financial_repl import financial_python_repl

prompt = get_prompt()

cfo_agent = Agent(
    model="gemini-2.5-flash",
    name="cfo_agent",
    description="CFO - Financial Analyst with Python access",
    instruction=prompt,
    tools=[financial_python_repl], 
    output_key="cfo_analysis"
)

# Wrap as Tool for the Coordinator
# cfo_tool = AgentTool(cfo_agent)
