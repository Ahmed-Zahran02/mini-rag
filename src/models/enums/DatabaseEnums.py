from enum import Enum

from pymongo.synchronous.collection import Collection


class DataBaseEnum(Enum):
    COLLECTION_PROJECT_NAME = "projects"
    COLLECTION_CHUNK_NAME = "chuncks"
    COLLECTION_ASSET_NAME = "assets"
