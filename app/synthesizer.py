from groq import Groq
from dotenv import load_dotenv
import os
import json

from app.schemas import ResearchResponse

load_dotenv(dotenv_path=".env")

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def synthesize_research(
    question: str,
    content_list: list[str],
    source_urls: list[str]
):

    combined_content = "\n\n".join(content_list)

    prompt = f"""
You are an AI research assistant.

Your job is to answer the user's question
using ONLY the provided research content.

You must synthesize information across
multiple sources instead of summarizing
a single article.

IMPORTANT RULES:

1. If the task is a comparison:
   - compare multiple entities
   - explain tradeoffs
   - avoid focusing on one product only
   - mention strengths and weaknesses

2. Do NOT summarize a single article.

3. Use cross-source reasoning.

4. Use ONLY the provided research content.

5. Mention uncertainty where appropriate.

6. Keep findings concise and actionable.

7. Do NOT copy article-specific or
marketing recommendations.

8. Suggested next steps must be:
   - generic
   - practical
   - research-oriented

GOOD examples:
- benchmark performance under realistic workloads
- compare pricing and operational complexity
- test scalability with representative datasets
- evaluate deployment tradeoffs

BAD examples:
- use product-specific calculators
- follow marketing tools
- copy article recommendations

9. Limitations should describe
uncertainty in the overall comparison,
not focus excessively on one vendor.

For comparison tasks, evaluate entities across:
- performance
- pricing
- scalability
- ease of deployment
- RAG suitability
- flexibility

Return ONLY valid JSON.

STRICT FORMAT RULES:

- question → string
- short_answer → concise comparison summary
- key_findings → list of strings
- sources_used → list of URLs
- confidence → "Low", "Medium", or "High"
- limitations → list of strings
- suggested_next_steps → list of strings

EXAMPLE GOOD BEHAVIOR:

Question:
Compare vector databases for RAG

Good Answer Style:
"Pinecone is best for managed production
deployments, Qdrant is lightweight and
startup-friendly, Weaviate supports hybrid
search, while Milvus is suitable for
enterprise-scale workloads."

USER QUESTION:
{question}

RESEARCH CONTENT:
{combined_content[:8000]}

SOURCES:
{source_urls}
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

        print("RAW SYNTHESIZER OUTPUT:")
        print(content)

        cleaned_content = content.strip()
        cleaned_content = cleaned_content.replace("```json", "")
        cleaned_content = cleaned_content.replace("```", "")
        cleaned_content = cleaned_content.strip()

        response_dict = json.loads(cleaned_content)

        validated_response = ResearchResponse(
            **response_dict
        )

        return validated_response

    except Exception as e:

        print(f"Synthesizer Error: {e}")
        return None