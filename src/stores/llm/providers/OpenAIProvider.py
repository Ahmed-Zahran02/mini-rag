import logging
from typing import Optional

from openai import OpenAI

from ..LLMEnums import OpenAIRoles
from ..LLMInterface import LLMInterface


class OpenAIProvider(LLMInterface):
    def __init__(
        self,
        api_key: str,
        base_url: str = None,
        max_input_characters: int = 1000,
        max_tokens: int = 1000,
        temperature: float = 0.2,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.max_input_characters = max_input_characters
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.generation_model = None
        self.embedding_model = None
        self.embedding_size = None
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_name: str):
        self.generation_model = model_name

    def set_embedding_model(self, model_name: str, embedding_size: int = 1536):
        self.embedding_model = model_name
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        if len(text) > self.max_input_characters:
            self.logger.warning(
                f"Input text exceeds maximum character limit of {self.max_input_characters}. Truncating."
            )
            return text[: self.max_input_characters]
        return text

    def embed_text(self, text: str, input_type: Optional[str]):
        if not self.embedding_model:
            self.logger.error("Embedding model is not set.")
            return None
        if not text:
            self.logger.warning("Input text is empty.")
            return None
        try:
            response = self.client.embeddings.create(
                input=text, model=self.embedding_model
            )
            return response.data[0].embedding
        except Exception as e:
            self.logger.error(f"Error in embedding text: {e}")
            return None

    def generate_text(
        self, prompt: str, max_tokens: int, temperature: float, history: list = []
    ) -> str:
        if not self.generation_model:
            self.logger.error("Generation model is not set.")
            return ""
        if not self.client:
            self.logger.error("OpenAI client is not initialized.")
            return ""
        try:
            history.append(self.construct_prompt(OpenAIRoles.USER.value, prompt))
            temperature = temperature if temperature is not None else self.temperature
            max_tokens = max_tokens if max_tokens is not None else self.max_tokens

            response = self.client.completions.create(
                model=self.generation_model,
                prompt=history,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            return response.choices[0].text.strip()
        except Exception as e:
            self.logger.error(f"Error in generating text: {e}")
            return ""

    def construct_prompt(self, role: str, content: str):
        return {"role": role, "content": content}
