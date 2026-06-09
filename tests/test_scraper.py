# tests/test_scraper.py

from unittest.mock import patch, Mock

from app.tools.scraper_tool import scrape_webpage


@patch("app.tools.scraper_tool.requests.get") # Mocking requests.get to avoid real HTTP calls during testing
def test_scraper_extracts_content(mock_get):

    mock_response = Mock()

    mock_response.text = """
    <html>
        <body>
            <p>Hello World</p>
            <p>Research Content</p>
        </body>
    </html>
    """

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    content = scrape_webpage("https://fake-url.com")

    assert "Hello World" in content
    assert "Research Content" in content