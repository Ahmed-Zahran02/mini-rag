import logging

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import InsertOne

from .BaseDataModel import BaseDataModel
from .db_schema import DataChunk
from .enums import DataBaseEnum


class ChunkModel(BaseDataModel):
    def __init__(self, db_client: AsyncIOMotorDatabase):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[  # pyright: ignore[reportIndexIssue]
            DataBaseEnum.COLLECTION_CHUNK_NAME.value
        ]

    async def init_collection_indexes(self):
        """Initialize indexes for the data chunk collection."""
        all_collections = (
            await self.db_client.list_collection_names()
        )  # pyright: ignore[reportAttributeAccessIssue]
        if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collections:
            await self.db_client.create_collection(  # pyright: ignore[reportAttributeAccessIssue]
                DataBaseEnum.COLLECTION_CHUNK_NAME.value
            )
            indexes = DataChunk.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"], name=index["name"], unique=index.get("unique", False)
                )

    @classmethod
    async def create_instance(cls, db_client):
        instance = cls(db_client)
        await instance.init_collection_indexes()
        return instance

    async def create_data_chunk(self, chunk: DataChunk) -> DataChunk:
        try:
            chunk_dict = chunk.model_dump(by_alias=True, exclude_unset=True)
            result = await self.collection.insert_one(chunk_dict)
            # return the chunk with the assigned _id
            return chunk.model_copy(update={"_id": str(result.inserted_id)})
        except Exception as e:
            logging.error(f"Error creating data chunk: {e}")
            raise e

    async def get_chunck_by_id(self, chunk_id: str) -> DataChunk | None:
        try:
            record = await self.collection.find_one({"_id": chunk_id})
            if record:
                return DataChunk(**record)
            return None
        except Exception as e:
            logging.error(f"Error retrieving data chunk by id: {e}")
            raise e

    async def insert_many_chunks(
        self, chunks: list[DataChunk], batch_size: int = 100
    ) -> list[str]:
        try:
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i : i + batch_size]
                operations = [
                    InsertOne(chunk.model_dump(by_alias=True, exclude_unset=True))
                    for chunk in batch
                ]
                result = await self.collection.bulk_write(operations)
                logging.info(
                    f"Inserted batch {i // batch_size + 1}: {result.inserted_count} chunks"
                )
            return [
                str(chunk.chunk_content) for chunk in chunks if chunk.id is not None
            ]
        except Exception as e:
            logging.error(f"Error inserting multiple data chunks: {e}")
            raise e

    async def clear_chunks_by_project_id(self, project_id: str) -> int:
        try:
            result = await self.collection.delete_many({"chunk_project_id": project_id})
            logging.info(
                f"Deleted {result.deleted_count} chunks for project_id {project_id}"
            )
            return result.deleted_count
        except Exception as e:
            logging.error(f"Error deleting chunks by project id: {e}")
            raise e

    async def get_chunks_by_project_id(
        self, project_id: str, page_no: int = 1, page_size: int = 1
    ) -> list[DataChunk]:
        """Retrieve chunks by project ID with pagination."""
        try:
            records = (
                self.collection.find({"chunk_project_id": project_id})
                .skip(page_size * (page_no - 1))
                .limit(page_size)
            )
            return [DataChunk(**record) async for record in records]
        except Exception as e:
            logging.error(f"Error retrieving chunks by project id: {e}")
            raise e
