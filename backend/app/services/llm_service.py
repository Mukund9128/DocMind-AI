import time
import requests
from flask import current_app


def complete(system, user):
    key = current_app.config['LLM_API_KEY']

    if not key:
        raise RuntimeError(
            'AI service is not configured.'
        )

    model = "gemini-3.7-flash"

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{model}:generateContent"
    )

    prompt = f"""SYSTEM INSTRUCTIONS:
{system}

USER REQUEST:
{user}
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2
        }
    }

    headers = {
        "x-goog-api-key": key,
        "Content-Type": "application/json"
    }

    # Try Gemini up to 3 times
    for attempt in range(3):

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=60
            )

        except requests.RequestException:

            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
                continue

            raise RuntimeError(
                "AI service is temporarily unavailable. "
                "Please try again later."
            )

        # Gemini success
        if response.ok:
            data = response.json()

            try:
                return (
                    data["candidates"][0]
                    ["content"]
                    ["parts"][0]
                    ["text"]
                )

            except (KeyError, IndexError, TypeError):
                raise RuntimeError(
                    "AI returned an unexpected response. "
                    "Please try again."
                )

        # Gemini quota exceeded
        if response.status_code == 429:
            raise RuntimeError(
                "AI usage limit reached. "
                "Please try again later."
            )

        # Gemini temporarily overloaded
        if response.status_code == 503:

            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
                continue

            raise RuntimeError(
                "AI service is temporarily busy. "
                "Please try again shortly."
            )

        # Other Gemini errors
        raise RuntimeError(
            "AI service encountered an error. "
            "Please try again later."
        )

    raise RuntimeError(
        "AI service is temporarily busy. "
        "Please try again shortly."
    )