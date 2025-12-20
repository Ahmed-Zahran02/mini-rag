import logging
from typing import Optional

import cohere

from ..LLMEnums import DocumentTypes, CoHereRoles
from ..LLMInterface import LLMInterface


class CoHereProvider(LLMInterface):
    def __init__(
        self,
        api_key: str,
        max_input_characters: int = 1000,
        max_tokens: int = 1000,
        temperature: float = 0.2,
    ):
        self.api_key = api_key
        self.max_input_characters = max_input_characters
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.generation_model = None
        self.embedding_model = None
        self.embedding_size = None
        self.co = cohere.ClientV2(self.api_key)
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

    def embed_text(self, text: str, input_type: str = DocumentTypes.DOCUMENT.value):
        if not self.embedding_model:
            self.logger.error("Embedding model is not set.")
            return None
        if not text:
            self.logger.warning("Input text is empty.")
            return None
        if input_type not in [item.value for item in DocumentTypes]:
            self.logger.warning(f"Input type {input_type} is not recognized.")
            return None
        try:
            response = self.co.embed(
                model=self.embedding_model, texts=[text], input_type=input_type
            )
            return response.embeddings.float_
        except Exception as e:
            self.logger.error(f"Error in embedding text: {e}")
            return None

    def generate_text(
        self,
        prompt: str,
        max_tokens: int = None,
        temperature: float = 0.5,
        history: Optional[list] = None,
    ) -> str:
        if not self.generation_model:
            self.logger.error("Generation model is not set.")
            return ""
        max_tokens = max_tokens if max_tokens is not None else self.max_tokens
        temperature = temperature if temperature is not None else self.temperature
        try:
            response = self.co.chat(
                model=self.generation_model,
                messages=[{"role": CoHereRoles.USER.value, "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            if response is None or not response.message or not response.message.content:
                self.logger.error("No response received from CoHere API.")
                return ""
            return response.message.content[0].text
        except Exception as e:
            self.logger.error(f"Error in generating text: {e}")
            return ""

    def construct_prompt(self, role: str, content: str) -> dict:
        return {"role": role, "text": content}
