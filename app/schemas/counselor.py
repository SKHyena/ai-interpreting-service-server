from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class CounselorCreate(BaseModel):
    counselor_user_id: str = Field(..., max_length=255)
    name: str = Field(..., max_length=255)
    email: EmailStr
    phone_number: Optional[str] = Field(None, max_length=20)
    password_hash: str = Field(..., max_length=512)
    employment_status: str = Field(..., max_length=50)
    institution_id: Optional[str] = Field(None, max_length=50)
    status: str = Field(..., max_length=50)


class CounselorResponse(CounselorCreate):
    created_at: datetime
    updated_at: datetime
