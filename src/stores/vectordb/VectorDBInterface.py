from abc import ABC, abstractmethod
from typing import Dict, List


class VectorDBInterface(ABC):
    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        pass

    @abstractmethod
    def create_collection(self, collection_name: str, distance: str) -> bool:
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def list_collections(self) -> List[str]:
        pass

    @abstractmethod
    def collection_exists(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def insert_one(
        self, collection_name: str, vector: List, metadata: Dict = None, id: str = None
    ) -> bool:
        pass

    @abstractmethod
    def insert_many(
        self,
        collection_name: str,
        vectors: List[List],
        metadatas: List[Dict] = None,
        ids: List[str] = None,
    ):
        pass
