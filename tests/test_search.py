from app.tools.search_tool import search_web


print("\nTESTING SEARCH TOOL...\n")

results = search_web(
    "best vector databases for RAG",
    max_results=3
)

for index, result in enumerate(results, start=1):

    print(f"\n========== RESULT {index} ==========")

    print("TITLE:")
    print(result["title"])

    print("\nURL:")
    print(result["url"])

    print("\nSNIPPET:")
    print(result["snippet"])