from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional


class DataChunk(BaseModel):
    id = Optional[str]
    chunk_content: str = Field(..., description="The content of the data chunk")
    chunk_order: int = Field(..., description="The order of the data chunk")
    chunk_type: str = Field(..., description="The type of the data chunk")
    chunk_project_id: ObjectId = Field(
        ..., description="The project ID of the data chunk"
    )
    chunk_metadata: dict = Field(..., description="The metadata of the data chunk")

    class Config:
        arbitrary_types_allowed = True
