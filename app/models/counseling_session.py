from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CounselingSession:
    counseling_session_id: Optional[int]  # 상담 세션 고유 식별자
    pairing_id: int  # 관련 페어링 ID
    counselor_user_id: str  # 상담원 사용자 ID
    counseling_type_id: int  # 상담 유형 ID
    session_start_time: Optional[datetime] = None  # 상담 시작 시간
    session_end_time: Optional[datetime] = None  # 상담 종료 시간
    status: str  # 상담 상태
    language_code: str  # 선택된 언어 코드
    created_at: Optional[datetime] = None  # 데이터 생성 시간
    updated_at: Optional[datetime] = None  # 데이터 수정 시간
