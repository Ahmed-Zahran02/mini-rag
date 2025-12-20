from typing import Dict

from .providers import QdrantDBProvider
from .VectorDBEnums import VectorDBType


class VectorDBFactory:
    def __init__(self, config):
        self.config = config

    def create(self, vectordb: str):
        if vectordb == VectorDBType.QDRANT.value:
            host = self.config.get("VECTORDB_HOST", "localhost")
            port = self.config.get("VECTORDB_PORT", 6333)
            return QdrantDBProvider(host=host, port=port)
