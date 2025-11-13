from google.adk.agents import ParallelAgent
from .agents.cso import cso_agent
from .agents.cmo import cmo_agent
from .agents.cfo import cfo_agent

# ============================================================================
# PARALLEL COUNCIL - All three analysts run simultaneously
# ============================================================================
parallel_council = ParallelAgent(
    name="parallel_council",
    description="CEMA Council executing parallel analysis",
    sub_agents=[
        cso_agent,  # Social impact (no tools)
        cmo_agent,  # Market analysis (google_search)
        cfo_agent   # Financial analysis (financial_python_repl)
    ]
)

# Expose for testing
root_agent = parallel_council

# from google.adk.agents import Agent, SequentialAgent, ParallelAgent
# from .agents.cso import cso_agent
# from .agents.cmo import cmo_tool 
# from .agents.cfo import cfo_tool


# # This agent sits inside the Parallel block. Its ONLY job is to run the tools.
# data_coordinator = Agent(
#     model="gemini-2.5-flash",
#     name="data_coordinator",
#     description="Manager of external data and financial tools",
#     instruction="""You are the Data Coordinator.
    
#     YOUR JOB:
#     Run the specialized tools to gather hard data for the decision.
    
#     INSTRUCTIONS:
#     1. Call `cmo_agent` to get market analysis.
#     2. Call `cfo_agent` to get financial analysis.
#     3. Output both reports clearly.
#     """,
#     tools=[cmo_tool, cfo_tool]
# )

# # parallel_analysts = ParallelAgent(
# #     name="parallel_analysts",
# #     description="Executes specialist agents in parallel",
# #     sub_agents=[
# #         cso_agent,
# #         # cfo_agent,  # Add when implemented
# #         # cro_agent,  # Add when implemented
# #         # cmo_agent,  # Add when implemented
# #     ]
# # )


# root_agent = Agent(
#     model='gemini-2.5-flash',
#     name='root_agent',
#     description='Orchestrator for CEMA Strategic Council.',
#     instruction='''You are the Orchestrator.
    
#     ROLES:
#     - Use `cso_agent` for Social Impact analysis (Mission, Vision, Values).
#     - Use `cmo_agent` for Market/Competitor analysis (Search, Business Model).
    
#     If the user asks for a full analysis, delegate to both sequentially.''',
#     tools=[cmo_tool],
#     sub_agents=[cso_agent,
# #         # cfo_agent,  # Add when implemented
# #         # cro_agent,  # Add when implemented
# #         # cmo_agent,  # Add when implemented
#     ]
# )

# # Final architecture (when CEO ready):
# # root_agent = SequentialAgent(
# #     name="cema_root",
# #     description="CEMA: parallel analysis + CEO synthesis",
# #     sub_agents=[
# #         parallel_analysts,  # Step 1: Parallel analysis
# #         ceo_agent,          # Step 2: CEO synthesis
# #     ]
# # )
