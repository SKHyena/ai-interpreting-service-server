from typing import List, Optional

import psycopg2

from ..models.language_group import LanguageGroup
from ..config import db_config


class LanguageGroupDAO:
    def __init__(self):
        self.db_config = db_config

    def _get_connection(self):
        return psycopg2.connect(**self.db_config)

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS aits.tb_language_groups (
            language_group_id SERIAL PRIMARY KEY,
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

    def insert_language_group(self, group: LanguageGroup) -> int:
        query = """
        INSERT INTO aits.tb_language_groups (
            institution_id, group_name
        ) VALUES (%s, %s)
        RETURNING language_group_id;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (group.institution_id, group.group_name))
                conn.commit()
                return cur.fetchone()[0]

    def get_language_group_by_id(self, language_group_id: int) -> Optional[LanguageGroup]:
        query = "SELECT * FROM aits.tb_language_groups WHERE language_group_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (language_group_id,))
                row = cur.fetchone()
                if row:
                    return LanguageGroup(
                        language_group_id=row[0],
                        institution_id=row[1],
                        group_name=row[2],
                        created_at=row[3],
                        updated_at=row[4],
                    )
                return None

    def get_all_language_groups(self) -> List[LanguageGroup]:
        query = "SELECT * FROM aits.tb_language_groups ORDER BY created_at DESC;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return [
                    LanguageGroup(
                        language_group_id=row[0],
                        institution_id=row[1],
                        group_name=row[2],
                        created_at=row[3],
                        updated_at=row[4],
                    ) for row in rows
                ]

    def update_language_group(self, language_group_id: int, updated_data: LanguageGroup) -> bool:
        query = """
        UPDATE aits.tb_language_groups
        SET institution_id = %s,
            group_name = %s
        WHERE language_group_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    updated_data.institution_id,
                    updated_data.group_name,
                    language_group_id
                ))
                conn.commit()
                return cur.rowcount > 0

    def delete_language_group(self, language_group_id: int) -> bool:
        query = "DELETE FROM aits.tb_language_groups WHERE language_group_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (language_group_id,))
                conn.commit()
                return cur.rowcount > 0

    def drop_table(self):
        query = "DROP TABLE IF EXISTS aits.tb_language_groups;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()
