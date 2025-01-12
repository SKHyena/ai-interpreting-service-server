from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CounselingTypeGroupCreate(BaseModel):
    institution_id: str = Field(..., max_length=50)
    group_name: str = Field(..., max_length=255)


class CounselingTypeGroupResponse(CounselingTypeGroupCreate):
    group_id: int
    created_at: datetime
    updated_at: datetime
