from app.planner import create_research_plan,get_groq_client
from app.tools.search_tool import search_web
from app.tools.scraper_tool import scrape_webpage
from app.tools.validator_tool import validate_content
from app.synthesizer import synthesize_research


def run_research_agent(query: str):

    print("\nSTEP 1: PLANNING")
    
    client = get_groq_client() # initialize client once and pass it to all components that need it

    plan = create_research_plan(
        query,
        client=client
    ) # pass the client to the planner for better testability
    
    if not plan:
        print("Planning failed")
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

            title = result.get("title", "").lower()

            # filter noisy/non-comparison pages
            query_keywords = query.lower().split()
            
            relevance_score = sum(
                1 for keyword in query_keywords if keyword in title
            ) 
            
            if relevance_score == 0:
                print(f"Skipped - low relevance (score: {relevance_score})")
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
                if url not in source_urls: # avoid duplicates
                    all_content.append(content)
                    source_urls.append(url)

            else:
                print("Skipped - validation failed")

    if not all_content:

        print("\nNo valid content found")

        return None
    
    # Dynamic decision: collect more evidence if needed

    if len(all_content) < 2: # 2 se kaam hua to aur content collect karte hai for better synthesis
        
        print("\nInsufficient evidence collected, expanding search...")
        
        if plan.task_type == "comparison": # if it's a comparison task, we want benchmarks to get more data points for comparison.
            extra_query = query + " benchmark"
            
        elif plan.task_type == "recommendation": # for recommendation, we want reviews to understand user sentiment and real-world performance.
            extra_query = query + " review"
            
        else:
            extra_query = query + " analysis" # for general research, we want in-depth analysis to get more comprehensive insights.
            
        extra_results = search_web(extra_query, max_results=2)
        
        for result in extra_results:

            url = result["url"]

            print(f"\nFetching content from: {url}")

            content = scrape_webpage(url)

            if not content:
                print("Skipping - no content")
                continue


            if validate_content(content):
                all_content.append(content)
                source_urls.append(url)

    print("\nSTEP 3: SYNTHESIS")
    
    final_response = synthesize_research(
        question=query,
        content_list=all_content,
        source_urls=source_urls,
        client=client # pass the client to the synthesizer for better testability
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