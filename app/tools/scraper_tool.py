import requests
from bs4 import BeautifulSoup


def scrape_webpage(url: str):

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        paragraphs = soup.find_all("p")

        content = ""

        for p in paragraphs:

            content += p.get_text() + "\n"

        cleaned_content = content.strip()

        return cleaned_content[:5000]

    except Exception as e:

        print(f"Scraper Error: {e}")

        return None