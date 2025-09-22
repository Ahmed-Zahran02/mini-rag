from pydantic import BaseModel
from typing import List, Optional


class DataSchema(BaseModel):
    file_id: str
    chunk_size: Optional[int] = 1000  # Default chunk size in KB
    overlap: Optional[int] = 10  # Default overlap size in KB
    de_reset: Optional[bool] = False  # Default is not to reset
