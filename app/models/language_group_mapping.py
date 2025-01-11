from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class LanguageGroupMapping:
    mapping_id: Optional[int] = None  # 매핑 고유 식별자
    language_group_id: int  # 언어 그룹 ID
    language_code: str  # 언어 코드
    created_at: Optional[datetime] = None  # 데이터 생성 시간
