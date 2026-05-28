from app.planner import create_research_plan
from app.tools.search_tool import search_web
from app.tools.scraper_tool import scrape_webpage
from app.tools.validator_tool import validate_content
from app.synthesizer import synthesize_research


def run_research_agent(query: str):

    print("\nSTEP 1: PLANNING")

    plan = create_research_plan(query)

    if not plan:
        return None

    print(plan)

    all_content = []
    source_urls = []

    print("\nSTEP 2: SEARCH + SCRAPE")

    # limit for faster testing
    for search_query in plan.search_queries[:2]:

        print(f"\nSearching for: {search_query}")

        search_results = search_web(
            search_query,
            max_results=2
        )

        for result in search_results:

            title = result["title"].lower()

            # filter noisy/non-comparison pages
            if (
                "comparison" not in title
                and "vs" not in title
                and "best" not in title
                and "benchmark" not in title
                and "top" not in title
            ):
                continue

            url = result["url"]

            print(f"\nFetching content from: {url}")

            content = scrape_webpage(url)

            if not content:
                print("Skipping - no content")
                continue

            is_valid = validate_content(content)

            if is_valid:

                print("Valid content found")

                all_content.append(content)
                source_urls.append(url)

            else:
                print("Skipped - validation failed")

    if not all_content:

        print("\nNo valid content found")

        return None

    print("\nSTEP 3: SYNTHESIS")
    
    final_response = synthesize_research(
        question=query,
        content_list=all_content,
        source_urls=source_urls
    )

    # confidence based on retrieval quality
    source_count = len(source_urls)

    if final_response:
        if source_count >= 3:
            final_response.confidence = "High"
        elif source_count == 2:
            final_response.confidence = "Medium"
        else:
            final_response.confidence = "Low"

    return final_response