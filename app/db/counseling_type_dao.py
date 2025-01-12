from typing import List, Optional

import psycopg2

from ..models.counseling_type import CounselingType
from ..config import db_config


class CounselingTypeDAO:
    def __init__(self):
        self.db_config = db_config

    def _get_connection(self):
        return psycopg2.connect(**self.db_config)

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS aits.tb_counseling_types (
            counseling_type_id SERIAL PRIMARY KEY,
            type_name VARCHAR(255) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()

    def insert_counseling_type(self, counseling_type: CounselingType) -> int:
        query = """
        INSERT INTO aits.tb_counseling_types (type_name, description)
        VALUES (%s, %s) RETURNING counseling_type_id;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (counseling_type.type_name, counseling_type.description))
                conn.commit()
                return cur.fetchone()[0]

    def get_counseling_type_by_id(self, counseling_type_id: int) -> Optional[CounselingType]:
        query = "SELECT * FROM aits.tb_counseling_types WHERE counseling_type_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (counseling_type_id,))
                row = cur.fetchone()
                if row:
                    return CounselingType(
                        counseling_type_id=row[0],
                        type_name=row[1],
                        description=row[2],
                        created_at=row[3],
                        updated_at=row[4],
                    )
                return None

    def get_all_counseling_types(self) -> List[CounselingType]:
        query = "SELECT * FROM aits.tb_counseling_types ORDER BY created_at DESC;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return [
                    CounselingType(
                        counseling_type_id=row[0],
                        type_name=row[1],
                        description=row[2],
                        created_at=row[3],
                        updated_at=row[4],
                    ) for row in rows
                ]

    def update_counseling_type(self, counseling_type_id: int, type_name: str, description: Optional[str]) -> bool:
        query = """
        UPDATE aits.tb_counseling_types
        SET type_name = %s, description = %s, updated_at = CURRENT_TIMESTAMP
        WHERE counseling_type_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (type_name, description, counseling_type_id))
                conn.commit()
                return cur.rowcount > 0

    def delete_counseling_type(self, counseling_type_id: int) -> bool:
        query = "DELETE FROM aits.tb_counseling_types WHERE counseling_type_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (counseling_type_id,))
                conn.commit()
                return cur.rowcount > 0

    def drop_table(self):
        query = "DROP TABLE IF EXISTS aits.tb_counseling_types;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()
