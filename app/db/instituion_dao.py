from typing import List, Optional

import psycopg2

from ..models.institution import Institution


class InstitutionDAO:
    def __init__(self, db_config: dict):
        self.db_config = db_config

    def _get_connection(self):
        return psycopg2.connect(**self.db_config)

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS aits.tb_institutions (
            institution_id VARCHAR(50) PRIMARY KEY,
            institution_name VARCHAR(255) NOT NULL,
            institution_address TEXT,
            institution_phone_number VARCHAR(20),
            institution_logo_path VARCHAR(512),
            institution_status VARCHAR(50) NOT NULL,
            operation_user_id VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()

    def insert_institution(self, institution: Institution) -> bool:
        query = """
        INSERT INTO aits.tb_institutions (
            institution_id, institution_name, institution_address,
            institution_phone_number, institution_logo_path,
            institution_status, operation_user_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    institution.institution_id,
                    institution.institution_name,
                    institution.institution_address,
                    institution.institution_phone_number,
                    institution.institution_logo_path,
                    institution.institution_status,
                    institution.operation_user_id
                ))
                conn.commit()
                return True

    def get_institution_by_id(self, institution_id: str) -> Optional[Institution]:
        query = "SELECT * FROM aits.tb_institutions WHERE institution_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (institution_id,))
                row = cur.fetchone()
                if row:
                    return Institution(
                        institution_id=row[0],
                        institution_name=row[1],
                        institution_address=row[2],
                        institution_phone_number=row[3],
                        institution_logo_path=row[4],
                        institution_status=row[5],
                        operation_user_id=row[6],
                        created_at=row[7],
                        updated_at=row[8]
                    )
                return None

    def get_all_institutions(self) -> List[Institution]:
        query = "SELECT * FROM aits.tb_institutions;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return [
                    Institution(
                        institution_id=row[0],
                        institution_name=row[1],
                        institution_address=row[2],
                        institution_phone_number=row[3],
                        institution_logo_path=row[4],
                        institution_status=row[5],
                        operation_user_id=row[6],
                        created_at=row[7],
                        updated_at=row[8]
                    ) for row in rows
                ]

    def update_institution(self, institution: Institution) -> bool:
        query = """
        UPDATE aits.tb_institutions
        SET institution_name = %s,
            institution_address = %s,
            institution_phone_number = %s,
            institution_logo_path = %s,
            institution_status = %s,
            operation_user_id = %s
        WHERE institution_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    institution.institution_name,
                    institution.institution_address,
                    institution.institution_phone_number,
                    institution.institution_logo_path,
                    institution.institution_status,
                    institution.operation_user_id,
                    institution.institution_id
                ))
                conn.commit()
                return cur.rowcount > 0

    def delete_institution(self, institution_id: str) -> bool:
        query = "DELETE FROM aits.tb_institutions WHERE institution_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (institution_id,))
                conn.commit()
                return cur.rowcount > 0

    def drop_table(self):
        query = "DROP TABLE IF EXISTS aits.tb_institutions;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()
