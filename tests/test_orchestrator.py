from unittest.mock import patch

from app.orchestrator import run_research_agent
from app.schemas import ResearchResponse


@patch("app.orchestrator.synthesize_research")
@patch("app.orchestrator.validate_content")
@patch("app.orchestrator.scrape_webpage")
@patch("app.orchestrator.search_web")
@patch("app.orchestrator.create_research_plan")
def test_orchestrator_pipeline(
    mock_plan,
    mock_search,
    mock_scrape,
    mock_validate,
    mock_synthesize
):

    mock_plan.return_value.search_queries = [
        "test query"
    ]

    mock_plan.return_value.task_type = "comparison"

    mock_search.return_value = [
        {
            "title": "test question comparison",
            "url": "https://example.com"
        }
    ]

    mock_scrape.return_value = (
        "Valid content " * 50
    )

    mock_validate.return_value = True

    mock_synthesize.return_value = ResearchResponse(
        question="test",
        short_answer="test answer",
        key_findings=["finding"],
        sources_used=["https://example.com"],
        confidence="Low",
        limitations=["none"],
        suggested_next_steps=["next step"]
    )

    result = run_research_agent(
        "test question"
    )

    assert result is not None
    assert result.question == "test"