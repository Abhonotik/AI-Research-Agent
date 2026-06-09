from app.tools.validator_tool import validate_content


def test_validator_rejects_empty_content():

    assert validate_content("") is False


def test_validator_rejects_short_content():

    assert validate_content("hello") is False


def test_validator_accepts_valid_content():

    content = "This is valid research content. " * 50

    assert validate_content(content) is True