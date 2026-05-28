from app.synthesizer import synthesize_research


print("\nTESTING SYNTHESIZER...\n")

content = [
    """
    Qdrant is lightweight and optimized for similarity search.
    It is startup-friendly and suitable for RAG systems.
    """,

    """
    Weaviate supports modules and hybrid search.
    It provides flexible integrations for AI applications.
    """
]

urls = [
    "https://qdrant.tech",
    "https://weaviate.io"
]

response = synthesize_research(
    question="Compare vector databases for RAG",
    content_list=content,
    source_urls=urls
)

print("\nSYNTHESIZER OUTPUT:\n")

print(response)