from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Counselor:
    counselor_user_id: str  # 상담원 사용자 ID
    name: str  # 상담원 이름
    email: str  # 상담원 이메일
    phone_number: Optional[str] = None  # 상담원 전화번호
    password_hash: str  # 비밀번호 해시
    employment_status: str  # 고용 상태
    institution_id: Optional[str] = None  # 소속 기관 ID
    status: str  # 상담원 상태
    created_at: Optional[datetime] = None  # 생성 시간
    updated_at: Optional[datetime] = None  # 수정 시간
