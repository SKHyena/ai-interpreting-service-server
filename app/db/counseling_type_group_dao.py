from typing import List, Optional

import psycopg2

from ..models.counseling_type_group import CounselingTypeGroup
from ..config import db_config


class CounselingTypeGroupDAO:
    def __init__(self):
        self.db_config = db_config

    def _get_connection(self):
        return psycopg2.connect(**self.db_config)

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS aits.tb_counseling_type_groups (
            group_id SERIAL PRIMARY KEY,
            institution_id VARCHAR(50) NOT NULL,
            group_name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()

    def insert_group(self, group: CounselingTypeGroup) -> int:
        query = """
        INSERT INTO aits.tb_counseling_type_groups (institution_id, group_name)
        VALUES (%s, %s) RETURNING group_id;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (group.institution_id, group.group_name))
                conn.commit()
                return cur.fetchone()[0]

    def get_group_by_id(self, group_id: int) -> Optional[CounselingTypeGroup]:
        query = "SELECT * FROM aits.tb_counseling_type_groups WHERE group_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (group_id,))
                row = cur.fetchone()
                if row:
                    return CounselingTypeGroup(
                        group_id=row[0],
                        institution_id=row[1],
                        group_name=row[2],
                        created_at=row[3],
                        updated_at=row[4],
                    )
                return None

    def get_all_groups(self) -> List[CounselingTypeGroup]:
        query = "SELECT * FROM aits.tb_counseling_type_groups ORDER BY created_at DESC;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return [
                    CounselingTypeGroup(
                        group_id=row[0],
                        institution_id=row[1],
                        group_name=row[2],
                        created_at=row[3],
                        updated_at=row[4],
                    ) for row in rows
                ]

    def update_group(self, group_id: int, institution_id: str, group_name: str) -> bool:
        query = """
        UPDATE aits.tb_counseling_type_groups
        SET institution_id = %s, group_name = %s, updated_at = CURRENT_TIMESTAMP
        WHERE group_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (institution_id, group_name, group_id))
                conn.commit()
                return cur.rowcount > 0

    def delete_group(self, group_id: int) -> bool:
        query = "DELETE FROM aits.tb_counseling_type_groups WHERE group_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (group_id,))
                conn.commit()
                return cur.rowcount > 0

    def drop_table(self):
        query = "DROP TABLE IF EXISTS aits.tb_counseling_type_groups;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()
