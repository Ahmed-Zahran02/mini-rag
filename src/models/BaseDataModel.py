from motor.motor_asyncio import AsyncIOMotorDatabase
from helpers.config import get_settings


class BaseDataModel:
    def __init__(self, db_client: AsyncIOMotorDatabase):
        self.settings = get_settings()
        self.db_client = db_client
