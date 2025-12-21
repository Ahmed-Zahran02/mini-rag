from typing import Dict

from .providers import QdrantDBProvider
from .VectorDBEnums import VectorDBType


class VectorDBFactory:
    def __init__(self, config):
        self.config = config

    def create(self, vectordb: str):
        if vectordb == VectorDBType.QDRANT.value:
            return QdrantDBProvider(
                vectordb_path=self.config.VECTORDB_PATH,
                embedding_size=self.config.EMBEDDING_SIZE,
            )
