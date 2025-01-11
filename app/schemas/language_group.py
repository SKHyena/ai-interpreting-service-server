from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class LanguageGroupCreate(BaseModel):
    institution_id: str = Field(..., max_length=50)
    group_name: str = Field(..., max_length=255)


class LanguageGroupResponse(LanguageGroupCreate):
    language_group_id: int
    created_at: datetime
    updated_at: datetime
