import requests
from app.core.config import settings

def generate_answer(prompt: str) -> str:
    """
    Sends a prompt to the LLM API and returns the generated answer.
    """
    url = settings.openrouter_api_url
    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": settings.openrouter_model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, json=payload, headers=headers, timeout=30)

    response.raise_for_status()
    return response.json().get("choices", [])[0].get("message", {}).get("content", "")