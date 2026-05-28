from app.planner import create_research_plan


print("\nTESTING PLANNER...\n")

plan = create_research_plan(
    "Compare top vector databases for RAG"
)

print("\nPLANNER OUTPUT:\n")

print(plan)