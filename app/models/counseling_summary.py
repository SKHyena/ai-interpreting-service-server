from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CounselingSummary:
    summary_id: Optional[int]  # 상담 요약 고유 식별자
    counseling_session_id: int  # 관련 상담 세션 ID
    counselor_user_id: str  # 상담원 사용자 ID
    counseling_type_id: int  # 상담 유형 ID
    pairing_id: int  # 관련 페어링 ID
    selected_language_code: str  # 선택된 언어 코드
    summary_text: str  # 상담 요약 내용
    conversation_log: Optional[str] = None  # 대화 기록 요약
    created_at: Optional[datetime] = None  # 데이터 생성 시간
    updated_at: Optional[datetime] = None  # 데이터 수정 시간
