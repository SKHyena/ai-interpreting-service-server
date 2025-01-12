from typing import List, Optional

import psycopg2

from ..models.counseling_session import CounselingSession
from ..config import db_config


class CounselingSessionDAO:
    def __init__(self):        
        self.db_config = db_config

    def _get_connection(self):
        return psycopg2.connect(**self.db_config)

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS aits.tb_counseling_sessions (
            counseling_session_id SERIAL PRIMARY KEY,
            pairing_id INT NOT NULL,
            counselor_user_id VARCHAR(255) NOT NULL,
            counseling_type_id INT NOT NULL,
            session_start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            session_end_time TIMESTAMP,
            status VARCHAR(50) NOT NULL,
            language_code VARCHAR(10) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()

    def insert_session(self, session: CounselingSession) -> int:
        query = """
        INSERT INTO aits.tb_counseling_sessions (
            pairing_id, counselor_user_id, counseling_type_id, session_start_time,
            session_end_time, status, language_code
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING counseling_session_id;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    session.pairing_id,
                    session.counselor_user_id,
                    session.counseling_type_id,
                    session.session_start_time,
                    session.session_end_time,
                    session.status,
                    session.language_code,
                ))
                conn.commit()
                return cur.fetchone()[0]

    def get_session_by_id(self, session_id: int) -> Optional[CounselingSession]:
        query = "SELECT * FROM aits.tb_counseling_sessions WHERE counseling_session_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (session_id,))
                row = cur.fetchone()
                if row:
                    return CounselingSession(
                        counseling_session_id=row[0],
                        pairing_id=row[1],
                        counselor_user_id=row[2],
                        counseling_type_id=row[3],
                        session_start_time=row[4],
                        session_end_time=row[5],
                        status=row[6],
                        language_code=row[7],
                        created_at=row[8],
                        updated_at=row[9],
                    )
                return None

    def get_all_sessions(self) -> List[CounselingSession]:
        query = "SELECT * FROM aits.tb_counseling_sessions ORDER BY created_at DESC;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return [
                    CounselingSession(
                        counseling_session_id=row[0],
                        pairing_id=row[1],
                        counselor_user_id=row[2],
                        counseling_type_id=row[3],
                        session_start_time=row[4],
                        session_end_time=row[5],
                        status=row[6],
                        language_code=row[7],
                        created_at=row[8],
                        updated_at=row[9],
                    ) for row in rows
                ]

    def update_session_status(self, session_id: int, status: str) -> bool:
        query = """
        UPDATE aits.tb_counseling_sessions
        SET status = %s, updated_at = CURRENT_TIMESTAMP
        WHERE counseling_session_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (status, session_id))
                conn.commit()
                return cur.rowcount > 0
    
    def update_session_status_by_pairing_id(self, pairing_id: int, status: str) -> bool:
        query = """
        UPDATE aits.tb_counseling_sessions
        SET status = %s, updated_at = CURRENT_TIMESTAMP
        WHERE pairing_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (status, pairing_id))
                conn.commit()
                return cur.rowcount > 0

    def delete_session(self, session_id: int) -> bool:
        query = "DELETE FROM aits.tb_counseling_sessions WHERE counseling_session_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (session_id,))
                conn.commit()
                return cur.rowcount > 0

    def drop_table(self):
        query = "DROP TABLE IF EXISTS aits.tb_counseling_sessions;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()
