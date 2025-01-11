from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PairingCreate(BaseModel):
    client_device_id: str = Field(..., max_length=255)
    counselor_device_id: Optional[str] = Field(None, max_length=255)
    counselor_user_id: Optional[str] = Field(None, max_length=255)
    pairing_code: str = Field(..., min_length=8, max_length=8)
    status: str = Field(..., max_length=50)
    counselor_pairing_time: Optional[datetime] = None


class PairingResponse(PairingCreate):
    pairing_id: int
    created_at: datetime
    updated_at: datetime
