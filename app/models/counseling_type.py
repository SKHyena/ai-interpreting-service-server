from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CounselingType:
    counseling_type_id: Optional[int]  # 상담 유형 고유 식별자
    type_name: str  # 상담 유형 이름
    description: Optional[str] = None  # 상담 유형 설명
    created_at: Optional[datetime] = None  # 데이터 생성 시간
    updated_at: Optional[datetime] = None  # 데이터 수정 시간
