from typing import List, Optional

import psycopg2

from ..models.language import Language


class LanguageDAO:
    def __init__(self, db_config: dict):
        self.db_config = db_config

    def _get_connection(self):
        return psycopg2.connect(**self.db_config)

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS aits.tb_languages (
            language_id SERIAL PRIMARY KEY,
            language_name VARCHAR(255) NOT NULL,
            language_code VARCHAR(10) UNIQUE NOT NULL,
            flag_path VARCHAR(512),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()

    def insert_language(self, language: Language) -> int:
        query = """
        INSERT INTO aits.tb_languages (
            language_name, language_code, flag_path
        ) VALUES (%s, %s, %s)
        RETURNING language_id;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    language.language_name,
                    language.language_code,
                    language.flag_path
                ))
                conn.commit()
                return cur.fetchone()[0]

    def get_language_by_id(self, language_id: int) -> Optional[Language]:
        query = "SELECT * FROM aits.tb_languages WHERE language_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (language_id,))
                row = cur.fetchone()
                if row:
                    return Language(
                        language_id=row[0],
                        language_name=row[1],
                        language_code=row[2],
                        flag_path=row[3],
                        created_at=row[4],
                        updated_at=row[5]
                    )
                return None

    def get_all_languages(self) -> List[Language]:
        query = "SELECT * FROM aits.tb_languages ORDER BY created_at DESC;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return [
                    Language(
                        language_id=row[0],
                        language_name=row[1],
                        language_code=row[2],
                        flag_path=row[3],
                        created_at=row[4],
                        updated_at=row[5]
                    ) for row in rows
                ]

    def update_language(self, language_id: int, updated_data: Language) -> bool:
        query = """
        UPDATE aits.tb_languages
        SET language_name = %s,
            language_code = %s,
            flag_path = %s
        WHERE language_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    updated_data.language_name,
                    updated_data.language_code,
                    updated_data.flag_path,
                    language_id
                ))
                conn.commit()
                return cur.rowcount > 0

    def delete_language(self, language_id: int) -> bool:
        query = "DELETE FROM aits.tb_languages WHERE language_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (language_id,))
                conn.commit()
                return cur.rowcount > 0

    def drop_table(self):
        query = "DROP TABLE IF EXISTS aits.tb_languages;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()
