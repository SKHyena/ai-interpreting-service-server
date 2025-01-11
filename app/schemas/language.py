from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class LanguageCreate(BaseModel):
    language_name: str = Field(..., max_length=255)
    language_code: str = Field(..., max_length=10)
    flag_path: Optional[str] = Field(None, max_length=512)


class LanguageResponse(LanguageCreate):
    language_id: int
    created_at: datetime
    updated_at: datetime
