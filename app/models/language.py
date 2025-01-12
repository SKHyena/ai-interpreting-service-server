from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Language:    
    language_name: str  # 언어 이름
    language_code: str  # 언어 코드
    language_id: Optional[int] = None  # 언어 고유 식별자 (자동 증가)
    flag_path: Optional[str] = None  # 국기 이미지 파일 경로
    created_at: Optional[datetime] = None  # 데이터 생성 시간
    updated_at: Optional[datetime] = None  # 데이터 수정 시간
