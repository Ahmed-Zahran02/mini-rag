from datetime import date, datetime
from decimal import DefaultContext
from email.policy import default

from bson import ObjectId
from pydantic import BaseModel, Field


class Asset(BaseModel):
    id: ObjectId = Field(..., default_factory=ObjectId, alias="_id")
    asset_project_id: ObjectId = Field(
        ..., description="Reference to the associated project"
    )
    asset_name: str = Field(..., description="Name of the asset")
    asset_time_created: datetime = Field(default_factory=datetime.now)
    asset_type: str = Field(..., min_length=1)
    asset_size: int = Field(ge=0, description="Size of the asset in bytes")

    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [("id", 1), ("asset_project_id", 1)],
                "name": "idx_asset_id_project_id",
                "unique": True,
            }
        ]
