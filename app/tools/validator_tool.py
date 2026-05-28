def validate_content(content: str):

    if not content:
        return False

    if len(content) < 300:
        return False

    spam_keywords = [
        "cookie policy",
        "enable javascript",
        "404"
    ]

    lower_content = content.lower()

    for keyword in spam_keywords:

        if keyword in lower_content:
            return False

    return True