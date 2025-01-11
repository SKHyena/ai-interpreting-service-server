from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CounselingChatLog:
    chat_id: Optional[int]  # 대화 고유 식별자
    counseling_session_id: int  # 상담 세션 ID
    sender_type: str  # 메시지 발신자 타입 (예: client, counselor)
    message: str  # 원본 대화 내용
    translated_message: Optional[str] = None  # 번역된 대화 내용
    client_message: Optional[str] = None  # 민원인이 작성한 메시지
    rag_applied_message: Optional[str] = None  # RAG가 적용된 메시지
    final_message: Optional[str] = None  # 확정된 메시지
    language_code: str  # 메시지의 언어 코드
    timestamp: Optional[datetime] = None  # 메시지 전송 시간
    created_at: Optional[datetime] = None  # 데이터 생성 시간
