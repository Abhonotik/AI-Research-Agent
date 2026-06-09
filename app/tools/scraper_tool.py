import time
import requests
from bs4 import BeautifulSoup


def scrape_webpage(url: str): #to search for content on the webpage
    max_retries = 3
    
    for attempt in range(max_retries):

        try:

            response = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0" # search block hojayega agar user agent nhi bheja tho. So we have to mimic.
                }
            )

            response.raise_for_status() # raise an exception for HTTP errors

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

            wait_time = 2 ** attempt # wait for 1, 2, 4 seconds before retrying

            print(
                f"Attempt {attempt + 1} failed: {e}"
            )

            if attempt < max_retries - 1: 

                print(
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

    print("All retries exhausted.")

    return None