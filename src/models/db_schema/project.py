from bson.objectid import ObjectId
from pydantic import BaseModel, Field, validator


class Project(BaseModel):
    id: ObjectId | None = Field(
        default_factory=ObjectId,
        alias="_id",
        description="The unique identifier of the project",
    )
    project_id: str = Field(..., min_length=2, max_length=100)

    @validator("project_id")
    def name_must_be_alphanum(cls, value):
        if not value[0].isalnum():
            raise ValueError("Name must be alphanumeric")
        return value

    class Config:
        arbitrary_types_allowed = True
