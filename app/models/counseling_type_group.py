from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CounselingTypeGroup:
    group_id: Optional[int]  # 상담 유형 그룹 고유 식별자
    institution_id: str  # 그룹이 속한 기관 ID
    group_name: str  # 상담 유형 그룹 이름
    created_at: Optional[datetime] = None  # 데이터 생성 시간
    updated_at: Optional[datetime] = None  # 데이터 수정 시간
