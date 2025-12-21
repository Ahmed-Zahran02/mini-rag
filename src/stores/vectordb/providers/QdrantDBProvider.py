import uuid
from logging import Logger
from typing import Dict, List

from qdrant_client import QdrantClient, models

from routes.schemas import RetrievedData

from ..VectorDBInterface import VectorDBInterface


class QdrantDBProvider(VectorDBInterface):
    def __init__(self, vectordb_path: str, embedding_size: int):
        self.db_path = vectordb_path
        self.client = QdrantClient(path=self.db_path)
        self.logger = Logger("__name__")
        self.embedding_size = embedding_size

    def connect(self) -> bool:
        try:
            if not self.client:
                self.client = QdrantClient(path=self.db_path)
            return True
        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            return False

    def disconnect(self) -> bool:
        if self.client:
            self.client.close()
        self.client = None
        return True

    def create_collection(
        self, collection_name: str, distance=models.Distance.COSINE
    ) -> bool:
        try:
            if not self.client:
                self.connect()
            if self.collection_exists(collection_name):
                self.logger.info(f"Collection {collection_name} already exists.")
                return True
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=self.embedding_size, distance=models.Distance.COSINE
                ),
            )
            return True
        except Exception as e:
            self.logger.error(f"Create collection error: {e}")
            return False

    def delete_collection(self, collection_name: str) -> bool:
        try:
            self.client.delete_collection(collection_name=collection_name)
            return True
        except Exception as e:
            self.logger.error(f"Delete collection error: {e}")
            return False

    def collection_exists(self, collection_name: str) -> bool:
        try:
            return self.client.collection_exists(collection_name=collection_name)
        except Exception as e:
            self.logger.error(f"Collection exists error: {e}")
            return False

    def list_collections(self) -> list:
        try:
            collections = self.client.get_collections()
            return [collection.name for collection in collections.collections]
        except Exception as e:
            self.logger.error(f"List collections error: {e}")
            return []

    def insert_one(
        self, collection_name: str, vector: list, metadata: dict = None, id: str = None
    ) -> bool:
        try:
            if not self.client:
                self.connect()
            if not self.collection_exists(collection_name):
                self.logger.info(f"Collection {collection_name} does not exist.")
                return False
            _ = self.client.upsert(
                collection_name=collection_name,
                points=[models.PointStruct(id=id, vector=vector, payload=metadata)],
            )
            return True
        except Exception as e:
            print(f"Insert one error: {e}")
            return False

    def insert_many(
        self,
        collection_name: str,
        vectors: list,
        metadatas: list = None,
        ids: list = None,
    ) -> bool:
        try:
            if not self.client:
                self.connect()
            if not self.collection_exists(collection_name):
                self.logger.info(f"Collection {collection_name} does not exist.")
                return False

            points = []
            for i in range(len(vectors)):
                payload = metadatas[i].copy() if metadatas and metadatas[i] else {}
                # Store original ID in metadata for reference
                if ids and ids[i]:
                    payload["original_id"] = ids[i]

                points.append(
                    models.PointStruct(
                        id=uuid.uuid4().hex,
                        vector=vectors[i],
                        payload=payload,
                    )
                )

            _ = self.client.upsert(
                collection_name=collection_name,
                points=points,
                wait=True,
            )
            return True
        except Exception as e:
            self.logger.error(f"Insert many error: {e}")
            return False

    def search_by_vector(
        self, collection_name: str, vector: List, limit: int = 3
    ) -> List[RetrievedData]:
        """Searches for similar vectors in the specified collection."""
        if not self.client:
            self.connect()
        if not self.collection_exists(collection_name):
            self.logger.info(f"Collection {collection_name} does not exist.")
            return []
        try:
            results = self.client.query_points(
                collection_name=collection_name,
                query=vector,
                limit=limit,
            ).points
            if not results:
                self.logger.info(
                    f"No results found for vector {vector} in collection {collection_name}."
                )

            return [
                RetrievedData(
                    text=result.payload.get("content", str(result.payload)),
                    score=result.score,
                )
                for result in results
            ]
        except Exception as e:
            self.logger.error(f"Search by vector error: {e}")
            return []

    def get_collection_info(self, collection_name: str) -> Dict:
        """Retrieves information about the specified collection."""
        if not self.client:
            self.connect()
        if not self.collection_exists(collection_name):
            self.logger.info(f"Collection {collection_name} does not exist.")
            return {}
        try:
            collection = self.client.get_collection(collection_name=collection_name)
            return {
                "status": collection.status,
                "indexed_vectors_count": collection.indexed_vectors_count,
                "points_count": collection.points_count,
                "segments_count": collection.segments_count,
            }
        except Exception as e:
            self.logger.error(f"Get collection info error: {e}")
            return {}
