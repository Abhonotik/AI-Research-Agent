from app.orchestrator import run_research_agent


print("\nSTARTING AI RESEARCH AGENT...\n")

response = run_research_agent(
    "Compare top vector databases for RAG"
)

print("\nFINAL RESPONSE:\n")

print(response)