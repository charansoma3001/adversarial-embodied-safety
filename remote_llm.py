
from typing import Collection, Mapping, Any, Sequence
import requests
import logging
from concordia.language_model import language_model

class RemoteLanguageModel(language_model.LanguageModel):
    def __init__(self, api_url: str, api_key: str = "sk-placeholder", model_name: str = "gpt-3.5-turbo"):
        self.api_url = api_url
        self.api_key = api_key
        self.model_name = model_name
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def sample_text(
        self,
        prompt: str,
        *,
        max_tokens: int = language_model.DEFAULT_MAX_TOKENS,
        terminators: Collection[str] = language_model.DEFAULT_TERMINATORS,
        temperature: float = language_model.DEFAULT_TEMPERATURE,
        top_p: float = language_model.DEFAULT_TOP_P,
        top_k: int = language_model.DEFAULT_TOP_K,
        timeout: float = language_model.DEFAULT_TIMEOUT_SECONDS,
        seed: int | None = None,
    ) -> str:
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "stop": list(terminators) if terminators else None,
        }
        
        # Check if the URL ends with /v1/chat/completions or just base URL
        endpoint = self.api_url
        if not endpoint.endswith("/chat/completions"):
             endpoint = f"{endpoint.rstrip('/')}/chat/completions"

        try:
            response = self._session.post(endpoint, json=payload, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            logging.error(f"Error calling LLM API: {e}")
            return "Error calling remote LLM."

    def sample_choice(
        self,
        prompt: str,
        responses: Sequence[str],
        *,
        seed: int | None = None,
    ) -> tuple[int, str, Mapping[str, Any]]:
        # Naive implementation of sample_choice using sample_text
        prompt_with_choices = prompt + "\nChoices:\n"
        for i, choice in enumerate(responses):
            prompt_with_choices += f"{i}. {choice}\n"
        prompt_with_choices += "Refuse to answer with anything other than the choice text. Respond with the chosen text exactly."
        
        result = self.sample_text(prompt_with_choices)
        
        best_choice = responses[0]
        best_idx = 0
        
        for i, choice in enumerate(responses):
            if choice in result:
                best_choice = choice
                best_idx = i
                break
                
        return best_idx, best_choice, {}
