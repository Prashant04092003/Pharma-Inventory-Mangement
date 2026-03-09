import requests
from app.core.settings import settings


class LLMClient:
    def __init__(self):
        self.base_url = f"{settings.OLLAMA_BASE_URL}/api/generate"
        self.model = settings.OLLAMA_MODEL
        self.timeout = settings.OLLAMA_TIMEOUT

    def generate(self, prompt: str, system: str = None) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        if system:
            payload["system"] = system

        response = requests.post(
            self.base_url,
            json=payload,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()