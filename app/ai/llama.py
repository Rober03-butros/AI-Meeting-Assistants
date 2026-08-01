import requests
from app.core.config import settings

OLLAMA_URL = settings.LLM_MODEL_URL

MODEL_NAME = settings.LLM_MODEL_NAME


def generate(prompt: str):

    response = requests.post(

        OLLAMA_URL,

        json={

            "model": MODEL_NAME,

            "prompt": prompt,

            "stream": False,

        },

    )

    if response.status_code != 200:
        print(response.text)
        raise Exception(response.text)
    
    response.raise_for_status()


    return response.json()["response"]