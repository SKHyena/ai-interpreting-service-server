from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CounselingSummaryCreate(BaseModel):
    counseling_session_id: int
    counselor_user_id: str = Field(..., max_length=255)
    counseling_type_id: int
    pairing_id: int
    selected_language_code: str = Field(..., max_length=10)
    summary_text: str
    conversation_log: Optional[str] = None


class CounselingSummaryResponse(CounselingSummaryCreate):
    summary_id: int
    created_at: datetime
    updated_at: datetime
