from abc import ABC, abstractmethod


class LLMInterface(ABC):
    @abstractmethod
    def set_generation_model(self, model_name: str):
        pass

    @abstractmethod
    def set_embedding_model(self, model_name: str):
        pass

    @abstractmethod
    def generate_text(
        self, prompt: str, max_tokens: int, temperature: float, history: list
    ) -> str:
        pass

    @abstractmethod
    def embed_text(self, text: str, input_type: str) -> list | None:
        pass

    @abstractmethod
    def construct_prompt(self, role: str, content: str) -> dict:
        pass
