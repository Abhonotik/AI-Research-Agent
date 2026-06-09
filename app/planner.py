from groq import Groq 
from dotenv import load_dotenv # to read .evn file 
import os
import json
import re
from app.schemas import ResearchPlan

load_dotenv(dotenv_path=".env")

def get_groq_client():  #jab tak client nhi pass hota, tab tak new client create karte raho.
    return Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

def create_research_plan(user_query: str,client=None):

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

        if client is None:
            client = get_groq_client()
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
            timeout=30
        )

        content = response.choices[0].message.content  # get the content of the message 0 is for the first choice

        print("RAW LLM OUTPUT:")
        print(content)

        cleaned_content = content.strip()
        cleaned_content = cleaned_content.replace("```json", "")
        cleaned_content = cleaned_content.replace("```", "")
        cleaned_content = cleaned_content.strip()

        print("\nCLEANED OUTPUT:")
        print(cleaned_content)
        
        json_match = re.search(r'\{.*\}', cleaned_content, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON object found in the LLM output.")
        
        plan_dict = json.loads(json_match.group())


        validated_plan = ResearchPlan(**plan_dict)

        return validated_plan

    except Exception as e:

        print(f"Planner Error: {e}")


# if rate limit error, return a basic plan with the original query as the only search query, and empty required information. This allows the agent to still function in a degraded mode, rather than failing completely.
        if "429" in str(e):
            print(
        "Rate limit reached."
    )
            
        else:print("planner unavailable.")
        
        return ResearchPlan(
            task_type="analysis",
            search_queries=[
                user_query,
                user_query + " analysis"],
            required_information=["overview"]
)