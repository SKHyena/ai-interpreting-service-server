from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CounselingChatLogCreate(BaseModel):
    counseling_session_id: int
    sender_type: str = Field(..., max_length=50)
    message: str
    translated_message: Optional[str] = None
    client_message: Optional[str] = None
    rag_applied_message: Optional[str] = None
    final_message: Optional[str] = None
    language_code: str = Field(..., max_length=10)


class CounselingChatLogResponse(CounselingChatLogCreate):
    chat_id: int
    timestamp: datetime
    created_at: datetime
