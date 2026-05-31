from ddgs import DDGS # DuckDuckGo Search API for web searching.

def search_web(query: str, max_results: int = 5):

    results_list = []

    try:

        with DDGS() as ddgs:   

            results = ddgs.text(  # actual search 
                query,
                max_results=max_results
            )

            for result in results:

                results_list.append({
                    "title": result.get("title"),
                    "url": result.get("href"),
                    "snippet": result.get("body")
                })

        return results_list

    except Exception as e:

        print(f"Search Tool Error: {e}")

        return []