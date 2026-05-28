from groq import Groq
from dotenv import load_dotenv
import os
import json

from app.schemas import ResearchPlan

load_dotenv(dotenv_path=".env")

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def create_research_plan(user_query: str):

    prompt = f"""
You are a research planning agent.

Your task is to create a high-quality research strategy.

Analyze the user's question carefully.

RULES:

1. Identify the research task type.

Possible task types:
- comparison
- explanation
- recommendation
- analysis
- trend_research

2. Generate SPECIFIC search queries.

BAD examples:
- AI agents
- vector databases
- RAG systems

GOOD examples:
- Pinecone vs Weaviate vs Qdrant comparison
- vector database benchmarks for RAG
- best vector database for startup RAG systems

3. If task is comparison:
- include entity-vs-entity searches
- include benchmark/comparison searches
- include tradeoff-focused searches

4. required_information should contain
specific research dimensions.

Example:
For comparison:
- pricing
- scalability
- performance
- latency
- deployment complexity
- use cases

Return ONLY valid JSON.

Required JSON schema:

{{
    "task_type": "string",
    "search_queries": [
        "string"
    ],
    "required_information": [
        "string"
    ]
}}

EXAMPLES:

Question:
Compare top vector databases for RAG

Output:
{{
    "task_type": "comparison",
    "search_queries": [
        "Pinecone vs Weaviate vs Qdrant comparison",
        "Milvus vs Pinecone benchmark",
        "best vector database for RAG",
        "vector database tradeoffs for RAG"
    ],
    "required_information": [
        "performance",
        "pricing",
        "scalability",
        "ease of deployment",
        "RAG suitability"
    ]
}}

Question:
Best AI coding assistants for startups

Output:
{{
    "task_type": "recommendation",
    "search_queries": [
        "Cursor vs GitHub Copilot comparison",
        "best AI coding assistants for startups",
        "AI coding assistant pricing comparison"
    ],
    "required_information": [
        "pricing",
        "features",
        "ease of use",
        "startup suitability"
    ]
}}

USER QUESTION:
{user_query}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        content = response.choices[0].message.content

        print("RAW LLM OUTPUT:")
        print(content)

        cleaned_content = content.strip()
        cleaned_content = cleaned_content.replace("```json", "")
        cleaned_content = cleaned_content.replace("```", "")
        cleaned_content = cleaned_content.strip()

        print("\nCLEANED OUTPUT:")
        print(cleaned_content)

        plan_dict = json.loads(cleaned_content)

        validated_plan = ResearchPlan(**plan_dict)

        return validated_plan

    except Exception as e:

        print(f"Planner Error: {e}")

        return None