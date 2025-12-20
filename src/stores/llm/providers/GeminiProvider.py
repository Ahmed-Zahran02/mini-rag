import logging
from typing import Optional

import google.generativeai as genai

from ..LLMEnums import GeminiInputTypes, GeminiRoles
from ..LLMInterface import LLMInterface


class GeminiProvider(LLMInterface):
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
        genai.configure(api_key=self.api_key)
        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_name: str):
        self.generation_model = model_name

    def set_embedding_model(self, model_name: str, embedding_size: int = 768):
        self.embedding_model = model_name
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        if len(text) > self.max_input_characters:
            self.logger.warning(
                f"Input text exceeds maximum character limit of {self.max_input_characters}. Truncating."
            )
            return text[: self.max_input_characters]
        return text

    def embed_text(
        self, text: str, input_type: str = GeminiInputTypes.SEMANTIC_SIMILARITY.value
    ):
        if not self.embedding_model:
            self.logger.error("Embedding model is not set.")
            return None
        if not text:
            self.logger.warning("Input text is empty.")
            return None
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type=input_type,
            )
            return result["embedding"]
        except Exception as e:
            self.logger.error(f"Error in embedding text: {e}")
            return None

    def generate_text(
        self,
        prompt: str,
        max_tokens: int = None,
        temperature: float = 1.0,
        history: Optional[list] = None,
    ) -> str:
        if not self.generation_model:
            self.logger.error("Generation model is not set.")
            return ""
        max_tokens = max_tokens if max_tokens is not None else self.max_tokens
        temperature = temperature if temperature is not None else self.temperature

        try:
            model = genai.GenerativeModel(self.generation_model)

            generation_config = genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature,
            )

            # Build chat history if provided
            chat_history = []
            if history:
                for message in history:
                    role = message.get("role", GeminiRoles.USER.value)
                    content = message.get("content", "")
                    # Gemini uses "user" and "model" roles
                    if role == "assistant":
                        role = GeminiRoles.ASSISTANT.value
                    chat_history.append({"role": role, "parts": [content]})

            if chat_history:
                chat = model.start_chat(history=chat_history)
                response = chat.send_message(
                    prompt, generation_config=generation_config
                )
            else:
                response = model.generate_content(
                    prompt,
                    generation_config=generation_config,
                )

            if response is None or not response.text:
                self.logger.error("No response received from Gemini API.")
                return ""

            return response.text.strip()
        except Exception as e:
            self.logger.error(f"Error in generating text: {e}")
            return ""

    def construct_prompt(self, role: str, content: str) -> dict:
        # Gemini uses "user" and "model" roles
        if role == "assistant":
            role = GeminiRoles.ASSISTANT.value
        return {"role": role, "content": content}
