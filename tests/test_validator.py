from app.tools.scraper_tool import scrape_webpage
from app.tools.validator_tool import validate_content


print("\nTESTING VALIDATOR TOOL...\n")

url = "https://www.ibm.com/think/topics/rag-vector-database"

content = scrape_webpage(url)

is_valid = validate_content(content)

print("\nVALIDATION RESULT:\n")

print(is_valid)