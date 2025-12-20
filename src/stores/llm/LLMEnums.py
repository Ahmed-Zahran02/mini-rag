from enum import Enum


class LLMProviderEnums(Enum):
    OPENAI = "openai"
    COHERE = "cohere"
    GEMINI = "gemini"


class OpenAIRoles(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class CoHereRoles(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class DocumentTypes(Enum):
    DOCUMENT = "search_document"
    QUERY = "search_query"
    CLASSIFICATION = "classification"
    CLUSTERING = "clustering"


class GeminiRoles(Enum):
    USER = "user"
    ASSISTANT = "model"


class GeminiInputTypes(Enum):
    RETRIEVAL_QUERY = "RETRIEVAL_QUERY"
    RETRIEVAL_DOCUMENT = "RETRIEVAL_DOCUMENT"
    SEMANTIC_SIMILARITY = "SEMANTIC_SIMILARITY"
    CLASSIFICATION = "CLASSIFICATION"
    CLUSTERING = "CLUSTERING"
