from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Institution:
    institution_id: str  # 기관 고유 식별자
    institution_name: str  # 기관 이름
    institution_address: Optional[str] = None  # 기관 주소 (Optional)
    institution_phone_number: Optional[str] = None  # 기관 전화번호 (Optional)
    institution_logo_path: Optional[str] = None  # 기관 로고 파일 경로 (Optional)
    institution_status: str  # 기관 상태 (예: active, inactive)
    operation_user_id: str  # 데이터 생성/수정한 사용자 ID
    created_at: Optional[datetime] = None  # 데이터 생성 시간
    updated_at: Optional[datetime] = None  # 데이터 수정 시간
