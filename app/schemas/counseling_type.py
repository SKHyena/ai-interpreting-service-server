from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CounselingTypeCreate(BaseModel):
    type_name: str = Field(..., max_length=255)
    description: Optional[str] = None


class CounselingTypeResponse(CounselingTypeCreate):
    counseling_type_id: int
    created_at: datetime
    updated_at: datetime
