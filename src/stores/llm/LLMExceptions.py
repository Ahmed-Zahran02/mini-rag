class LLMException(Exception):
    """Base exception for LLM operations."""

    pass


class EmbeddingException(LLMException):
    """Exception raised when embedding generation fails."""

    pass


class GenerationException(LLMException):
    """Exception raised when text generation fails."""

    pass
