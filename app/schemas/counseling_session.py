from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CounselingSessionCreate(BaseModel):
    pairing_id: int
    counselor_user_id: str = Field(..., max_length=255)
    counseling_type_id: int
    session_start_time: Optional[datetime] = None
    session_end_time: Optional[datetime] = None
    status: str = Field(..., max_length=50)
    language_code: str = Field(..., max_length=10)


class CounselingSessionResponse(CounselingSessionCreate):
    counseling_session_id: int
    created_at: datetime
    updated_at: datetime
