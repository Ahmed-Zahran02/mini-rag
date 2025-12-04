from bson.objectid import ObjectId
from pydantic import BaseModel, Field, field_validator


class Project(BaseModel):
    id: ObjectId = Field(
        default_factory=ObjectId,
        alias="_id",
        description="The unique identifier of the project",
    )
    project_id: str = Field(..., min_length=1, max_length=100)

    @field_validator("project_id")
    def name_must_be_alphanum(cls, value):
        if not value[0].isalnum():
            raise ValueError("Name must be alphanumeric")
        return value

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        return [{"key": [("project_id", 1)], "name": "idx_project_id", "unique": True}]
