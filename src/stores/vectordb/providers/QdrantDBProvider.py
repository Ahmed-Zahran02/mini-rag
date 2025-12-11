from logging import Logger

from qdrant_client import QdrantClient, models

from ..VectorDBInterface import VectorDBInterface


class QdrantDBProvider(VectorDBInterface):
    def __init__(self, host: str = "localhost", port: int = 6333):
        self.host = host
        self.port = port
        self.client = QdrantClient(host=self.host, port=self.port)
        self.logger = Logger("__name__")

    def connect(self) -> bool:
        try:
            self.client = QdrantClient(host=self.host, port=self.port)
            return True
        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            return False

    def disconnect(self) -> bool:
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
                vectors=models.VectorParams(size=1536, distance=models.Distance.COSINE),
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

            _ = self.client.upsert(
                collection_name=collection_name,
                points=[
                    models.PointStruct(
                        id=ids[i] if ids else None,
                        vector=vectors[i],
                        payload=metadatas[i] if metadatas else None,
                    )
                    for i in range(len(vectors))
                ],
            )
            return True
        except Exception as e:
            self.logger.error(f"Insert many error: {e}")
            return False
