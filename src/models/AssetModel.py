import logging

from .BaseDataModel import BaseDataModel
from .db_schema import Asset
from .enums import DataBaseEnum


class AssetModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]

    async def init_collection(self):
        all_collections = self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:
            await self.db_client.create_collection(
                DataBaseEnum.COLLECTION_ASSET_NAME.value
            )
            indexes = Asset.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    key=index["key"],
                    name=index["name"],
                    unique=index.get("unique", False),
                )

    @classmethod
    async def create_instance(cls, db_client):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def create_asset(self, asset: Asset):
        try:
            await self.collection.insert_one(
                asset.model_dump(by_alias=True, exclude_unset=True)
            )
            return asset
        except Exception as e:
            logging.error(f"Error creating asset: {e}")
            raise e

    async def get_project_assets(self, asset_project_id):
        try:
            cursor = await self.collection.find({"asset_project_id": asset_project_id})
            assets = []
            async for doc in cursor:
                assets.append(Asset(**doc))
            return assets
        except Exception as e:
            logging.error(
                f"Error retrieving assets for project {asset_project_id}: {e}"
            )
            raise e
