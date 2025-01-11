from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class InstitutionCreate(BaseModel):
    institution_id: str = Field(..., max_length=50)
    institution_name: str = Field(..., max_length=255)
    institution_address: Optional[str]
    institution_phone_number: Optional[str]
    institution_logo_path: Optional[str]
    institution_status: str = Field(..., max_length=50)
    operation_user_id: str = Field(..., max_length=255)

class InstitutionResponse(InstitutionCreate):
    created_at: datetime
    updated_at: datetime
