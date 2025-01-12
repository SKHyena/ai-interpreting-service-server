from typing import List, Optional

import psycopg2

from ..models.counselor import Counselor
from ..config import db_config


class CounselorDAO:
    def __init__(self):
        self.db_config = db_config

    def _get_connection(self):
        return psycopg2.connect(**self.db_config)

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS aits.tb_counselors (
            counselor_user_id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            phone_number VARCHAR(20),
            password_hash VARCHAR(512) NOT NULL,
            employment_status VARCHAR(50) NOT NULL,
            institution_id VARCHAR(50),
            status VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()

    def insert_counselor(self, counselor: Counselor) -> str:
        query = """
        INSERT INTO aits.tb_counselors (
            counselor_user_id, name, email, phone_number, password_hash,
            employment_status, institution_id, status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING counselor_user_id;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    counselor.counselor_user_id,
                    counselor.name,
                    counselor.email,
                    counselor.phone_number,
                    counselor.password_hash,
                    counselor.employment_status,
                    counselor.institution_id,
                    counselor.status,
                ))
                conn.commit()
                return cur.fetchone()[0]

    def get_counselor_by_id(self, counselor_user_id: str) -> Optional[Counselor]:
        query = "SELECT * FROM aits.tb_counselors WHERE counselor_user_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (counselor_user_id,))
                row = cur.fetchone()
                if row:
                    return Counselor(
                        counselor_user_id=row[0],
                        name=row[1],
                        email=row[2],
                        phone_number=row[3],
                        password_hash=row[4],
                        employment_status=row[5],
                        institution_id=row[6],
                        status=row[7],
                        created_at=row[8],
                        updated_at=row[9],
                    )
                return None

    def get_all_counselors(self) -> List[Counselor]:
        query = "SELECT * FROM aits.tb_counselors ORDER BY created_at DESC;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return [
                    Counselor(
                        counselor_user_id=row[0],
                        name=row[1],
                        email=row[2],
                        phone_number=row[3],
                        password_hash=row[4],
                        employment_status=row[5],
                        institution_id=row[6],
                        status=row[7],
                        created_at=row[8],
                        updated_at=row[9],
                    ) for row in rows
                ]

    def update_counselor(self, counselor_user_id: str, updated_data: Counselor) -> bool:
        query = """
        UPDATE aits.tb_counselors
        SET name = %s, email = %s, phone_number = %s, password_hash = %s,
            employment_status = %s, institution_id = %s, status = %s
        WHERE counselor_user_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    updated_data.name,
                    updated_data.email,
                    updated_data.phone_number,
                    updated_data.password_hash,
                    updated_data.employment_status,
                    updated_data.institution_id,
                    updated_data.status,
                    counselor_user_id,
                ))
                conn.commit()
                return cur.rowcount > 0

    def delete_counselor(self, counselor_user_id: str) -> bool:
        query = "DELETE FROM aits.tb_counselors WHERE counselor_user_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (counselor_user_id,))
                conn.commit()
                return cur.rowcount > 0

    def drop_table(self):
        query = "DROP TABLE IF EXISTS aits.tb_counselors;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()
