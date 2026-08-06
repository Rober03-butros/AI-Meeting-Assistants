import requests
from app.core.config import settings

OLLAMA_URL = settings.LLM_MODEL_URL

MODEL_NAME = settings.LLM_MODEL_NAME


def generate(
    prompt: str,
    system: str | None = None,
    temperature: float = 0.0,
):

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
        },
    }

    if system is not None:
        payload["system"] = system

    response = requests.post(
        OLLAMA_URL,
        json=payload,
    )

    if response.status_code != 200:
        print(response.text)
        raise RuntimeError(response.text)

    return response.json()["response"].strip()