from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class LanguageGroup:    
    institution_id: str  # 관련 기관 ID
    group_name: str  # 언어 그룹 이름
    language_group_id: Optional[int] = None  # 언어 그룹 고유 식별자
    created_at: Optional[datetime] = None  # 데이터 생성 시간
    updated_at: Optional[datetime] = None  # 데이터 수정 시간
