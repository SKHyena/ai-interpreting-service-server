from typing import List, Optional

import psycopg2

from ..models.language_group_mapping import LanguageGroupMapping
from ..config import db_config


class LanguageGroupMappingDAO:
    def __init__(self):
        self.db_config = db_config

    def _get_connection(self):
        return psycopg2.connect(**self.db_config)

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS aits.tb_language_group_mappings (
            mapping_id SERIAL PRIMARY KEY,
            language_group_id INT NOT NULL,
            language_code VARCHAR(10) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()

    def insert_mapping(self, mapping: LanguageGroupMapping) -> int:
        query = """
        INSERT INTO aits.tb_language_group_mappings (
            language_group_id, language_code
        ) VALUES (%s, %s)
        RETURNING mapping_id;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (mapping.language_group_id, mapping.language_code))
                conn.commit()
                return cur.fetchone()[0]

    def get_mapping_by_id(self, mapping_id: int) -> Optional[LanguageGroupMapping]:
        query = "SELECT * FROM aits.tb_language_group_mappings WHERE mapping_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (mapping_id,))
                row = cur.fetchone()
                if row:
                    return LanguageGroupMapping(
                        mapping_id=row[0],
                        language_group_id=row[1],
                        language_code=row[2],
                        created_at=row[3],
                    )
                return None

    def get_all_mappings(self) -> List[LanguageGroupMapping]:
        query = "SELECT * FROM aits.tb_language_group_mappings ORDER BY created_at DESC;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return [
                    LanguageGroupMapping(
                        mapping_id=row[0],
                        language_group_id=row[1],
                        language_code=row[2],
                        created_at=row[3],
                    ) for row in rows
                ]

    def update_mapping(self, mapping_id: int, updated_data: LanguageGroupMapping) -> bool:
        query = """
        UPDATE aits.tb_language_group_mappings
        SET language_group_id = %s,
            language_code = %s
        WHERE mapping_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    updated_data.language_group_id,
                    updated_data.language_code,
                    mapping_id
                ))
                conn.commit()
                return cur.rowcount > 0

    def delete_mapping(self, mapping_id: int) -> bool:
        query = "DELETE FROM aits.tb_language_group_mappings WHERE mapping_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (mapping_id,))
                conn.commit()
                return cur.rowcount > 0

    def drop_table(self):
        query = "DROP TABLE IF EXISTS aits.tb_language_group_mappings;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()
