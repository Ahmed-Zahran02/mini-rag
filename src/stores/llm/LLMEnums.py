from enum import Enum


class LLMProviderEnums(Enum):
    OPENAI = "openai"
    COHERE = "cohere"


class OpenAIRoles(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class CoHereRoles(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class CoHereInputTypes(Enum):
    DOCUMENT = "search_document"
    QUERY = "search_query"
    CLASSIFICATION = "classification"
    CLUSTERING = "clustering"
