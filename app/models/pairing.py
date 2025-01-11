from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Pairing:
    pairing_id: Optional[int]  # 페어링 고유 식별자
    client_device_id: str  # 민원인 앱의 디바이스 ID
    counselor_device_id: Optional[str]  # 상담원 앱의 디바이스 ID
    counselor_user_id: Optional[str]  # 상담원 사용자 ID
    pairing_code: str  # 페어링 코드 (8자리 숫자 난수)
    status: str  # 페어링 상태
    counselor_pairing_time: Optional[datetime]  # 상담원 앱 페어링 시간
    created_at: Optional[datetime] = None  # 생성 시간
    updated_at: Optional[datetime] = None  # 수정 시간
