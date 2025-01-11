from pydantic import BaseModel, Field
from datetime import datetime


class LanguageGroupMappingCreate(BaseModel):
    language_group_id: int
    language_code: str = Field(..., max_length=10)


class LanguageGroupMappingResponse(LanguageGroupMappingCreate):
    mapping_id: int
    created_at: datetime
