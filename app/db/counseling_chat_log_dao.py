from typing import List, Optional

import psycopg2

from ..models.counseling_chat_log import CounselingChatLog

class CounselingChatLogDAO:
    def __init__(self, db_config: dict):
        self.db_config = db_config

    def _get_connection(self):
        return psycopg2.connect(**self.db_config)

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS aits.tb_counseling_chat_logs (
            chat_id SERIAL PRIMARY KEY,
            counseling_session_id INT NOT NULL,
            sender_type VARCHAR(50) NOT NULL,
            message TEXT NOT NULL,
            translated_message TEXT,
            client_message TEXT,
            rag_applied_message TEXT,
            final_message TEXT,
            language_code VARCHAR(10) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()

    def insert_chat_log(self, chat_log: CounselingChatLog) -> int:
        query = """
        INSERT INTO aits.tb_counseling_chat_logs (
            counseling_session_id, sender_type, message, translated_message,
            client_message, rag_applied_message, final_message, language_code
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING chat_id;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    chat_log.counseling_session_id,
                    chat_log.sender_type,
                    chat_log.message,
                    chat_log.translated_message,
                    chat_log.client_message,
                    chat_log.rag_applied_message,
                    chat_log.final_message,
                    chat_log.language_code,
                ))
                conn.commit()
                return cur.fetchone()[0]

    def get_chat_log_by_id(self, chat_id: int) -> Optional[CounselingChatLog]:
        query = "SELECT * FROM aits.tb_counseling_chat_logs WHERE chat_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (chat_id,))
                row = cur.fetchone()
                if row:
                    return CounselingChatLog(
                        chat_id=row[0],
                        counseling_session_id=row[1],
                        sender_type=row[2],
                        message=row[3],
                        translated_message=row[4],
                        client_message=row[5],
                        rag_applied_message=row[6],
                        final_message=row[7],
                        language_code=row[8],
                        timestamp=row[9],
                        created_at=row[10],
                    )
                return None

    def get_all_chat_logs(self) -> List[CounselingChatLog]:
        query = "SELECT * FROM aits.tb_counseling_chat_logs ORDER BY created_at DESC;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return [
                    CounselingChatLog(
                        chat_id=row[0],
                        counseling_session_id=row[1],
                        sender_type=row[2],
                        message=row[3],
                        translated_message=row[4],
                        client_message=row[5],
                        rag_applied_message=row[6],
                        final_message=row[7],
                        language_code=row[8],
                        timestamp=row[9],
                        created_at=row[10],
                    ) for row in rows
                ]

    def update_chat_log(self, chat_id: int, final_message: str) -> bool:
        query = """
        UPDATE aits.tb_counseling_chat_logs
        SET final_message = %s, timestamp = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
        WHERE chat_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (final_message, chat_id))
                conn.commit()
                return cur.rowcount > 0

    def delete_chat_log(self, chat_id: int) -> bool:
        query = "DELETE FROM aits.tb_counseling_chat_logs WHERE chat_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (chat_id,))
                conn.commit()
                return cur.rowcount > 0

    def drop_table(self):
        query = "DROP TABLE IF EXISTS aits.tb_counseling_chat_logs;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()
