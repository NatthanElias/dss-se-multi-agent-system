from google.adk.agents import SequentialAgent, ParallelAgent
from .agents.cso import cso_agent
from .agents.cmo import cmo_agent
from .agents.cfo import cfo_agent
from .agents.cro import cro_agent
from .agents.ceo import ceo_agent
from .config import config


# Build sub_agents list based on enabled agents
sub_agents = []

if config.agents.enable_cso:
    sub_agents.append(cso_agent)
if config.agents.enable_cmo:
    sub_agents.append(cmo_agent)
if config.agents.enable_cfo:
    sub_agents.append(cfo_agent)
if config.agents.enable_cro:
    sub_agents.append(cro_agent)

parallel_council = ParallelAgent(
    name="parallel_council",
    description="CEMA Executive Council executing parallel analysis",
    sub_agents=sub_agents
)

if config.agents.enable_ceo:
    root_agent = SequentialAgent(
        name="cema_root",
        description="CEMA: Parallel council analysis followed by CEO synthesis",
        sub_agents=[
            parallel_council,  # Step 1: Parallel analysis (CSO, CMO, CFO, CRO)
            ceo_agent          # Step 2: CEO synthesizes and decides
        ]
    )
else:
    # If CEO disabled, just return council results
    root_agent = parallel_council
