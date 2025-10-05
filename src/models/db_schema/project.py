from pydantic import BaseModel, Field, validator
from typing import Optional
from bson import ObjectId


class Project(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId)
    name: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=2, max_length=500)

    @validator("name")
    def name_must_be_alphanum(cls, value):
        if not value[0].isalnum():
            raise ValueError("Name must be alphanumeric")
        return value

    class Config:
        arbitrary_types_allowed = True
