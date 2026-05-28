from app.tools.scraper_tool import scrape_webpage


print("\nTESTING SCRAPER TOOL...\n")

url = "https://www.ibm.com/think/topics/rag-vector-database"

content = scrape_webpage(url)

print("\nSCRAPED CONTENT:\n")

print(content[:3000])