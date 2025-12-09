from .providers import OpenAIProvider, CoHereProvider
from .LLMEnums import LLMProviderEnums


class LLMProviderFactory:
    def __init__(self, config):
        self.config = config

    def get_provider(self, provider_name: str):
        if provider_name == LLMProviderEnums.OPENAI.value:
            return OpenAIProvider(
                api_key=self.config.OPENAI_API_KEY, base_url=self.config.OPENAI_BASE_URL,
                max_input_characters=self.config.MAX_INPUT_CHARACTERS,
                max_tokens=self.config.MAX_TOKENS,
                temperature=self.config.TEMPERATURE,
            )
        elif provider_name == LLMProviderEnums.COHERE.value:
            return CoHereProvider(api_key=self.config.COHERE_API_KEY, 
                max_input_characters=self.config.MAX_INPUT_CHARACTERS,
                max_tokens=self.config.MAX_TOKENS,
                temperature=self.config.TEMPERATURE,
            )
        return None
