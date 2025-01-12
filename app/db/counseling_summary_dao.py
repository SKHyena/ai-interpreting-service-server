from typing import List, Optional

import psycopg2

from ..models.counseling_summary import CounselingSummary
from ..config import db_config


class CounselingSummaryDAO:
    def __init__(self):
        self.db_config = db_config

    def _get_connection(self):
        return psycopg2.connect(**self.db_config)

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS aits.tb_counseling_summaries (
            summary_id SERIAL PRIMARY KEY,
            counseling_session_id INT NOT NULL,
            counselor_user_id VARCHAR(255) NOT NULL,
            counseling_type_id INT NOT NULL,
            pairing_id INT NOT NULL,
            selected_language_code VARCHAR(10) NOT NULL,
            summary_text TEXT NOT NULL,
            conversation_log TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()

    def insert_summary(self, summary: CounselingSummary) -> int:
        query = """
        INSERT INTO aits.tb_counseling_summaries (
            counseling_session_id, counselor_user_id, counseling_type_id, pairing_id,
            selected_language_code, summary_text, conversation_log
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING summary_id;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    summary.counseling_session_id,
                    summary.counselor_user_id,
                    summary.counseling_type_id,
                    summary.pairing_id,
                    summary.selected_language_code,
                    summary.summary_text,
                    summary.conversation_log,
                ))
                conn.commit()
                return cur.fetchone()[0]

    def get_summary_by_id(self, summary_id: int) -> Optional[CounselingSummary]:
        query = "SELECT * FROM aits.tb_counseling_summaries WHERE summary_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (summary_id,))
                row = cur.fetchone()
                if row:
                    return CounselingSummary(
                        summary_id=row[0],
                        counseling_session_id=row[1],
                        counselor_user_id=row[2],
                        counseling_type_id=row[3],
                        pairing_id=row[4],
                        selected_language_code=row[5],
                        summary_text=row[6],
                        conversation_log=row[7],
                        created_at=row[8],
                        updated_at=row[9],
                    )
                return None

    def get_all_summaries(self) -> List[CounselingSummary]:
        query = "SELECT * FROM aits.tb_counseling_summaries ORDER BY created_at DESC;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return [
                    CounselingSummary(
                        summary_id=row[0],
                        counseling_session_id=row[1],
                        counselor_user_id=row[2],
                        counseling_type_id=row[3],
                        pairing_id=row[4],
                        selected_language_code=row[5],
                        summary_text=row[6],
                        conversation_log=row[7],
                        created_at=row[8],
                        updated_at=row[9],
                    ) for row in rows
                ]

    def update_summary(self, summary_id: int, summary_text: str, conversation_log: Optional[str] = None) -> bool:
        query = """
        UPDATE aits.tb_counseling_summaries
        SET summary_text = %s, conversation_log = %s, updated_at = CURRENT_TIMESTAMP
        WHERE summary_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (summary_text, conversation_log, summary_id))
                conn.commit()
                return cur.rowcount > 0

    def delete_summary(self, summary_id: int) -> bool:
        query = "DELETE FROM aits.tb_counseling_summaries WHERE summary_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (summary_id,))
                conn.commit()
                return cur.rowcount > 0

    def drop_table(self):
        query = "DROP TABLE IF EXISTS aits.tb_counseling_summaries;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()
