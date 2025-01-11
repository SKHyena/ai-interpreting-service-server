from typing import List, Optional

import psycopg2

from ..models.pairing import Pairing


class PairingDAO:
    def __init__(self, db_config: dict):
        self.db_config = db_config

    def _get_connection(self):
        return psycopg2.connect(**self.db_config)

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS aits.tb_pairings (
            pairing_id SERIAL PRIMARY KEY,
            client_device_id VARCHAR(255) NOT NULL,
            counselor_device_id VARCHAR(255),
            counselor_user_id VARCHAR(255),
            pairing_code CHAR(8) NOT NULL,
            status VARCHAR(50) NOT NULL,
            counselor_pairing_time TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()

    def insert_pairing(self, pairing: Pairing) -> int:
        query = """
        INSERT INTO aits.tb_pairings (
            client_device_id, counselor_device_id, counselor_user_id,
            pairing_code, status, counselor_pairing_time
        ) VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING pairing_id;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    pairing.client_device_id,
                    pairing.counselor_device_id,
                    pairing.counselor_user_id,
                    pairing.pairing_code,
                    pairing.status,
                    pairing.counselor_pairing_time,
                ))
                conn.commit()
                return cur.fetchone()[0]

    def get_pairing_by_id(self, pairing_id: int) -> Optional[Pairing]:
        query = "SELECT * FROM aits.tb_pairings WHERE pairing_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (pairing_id,))
                row = cur.fetchone()
                if row:
                    return Pairing(
                        pairing_id=row[0],
                        client_device_id=row[1],
                        counselor_device_id=row[2],
                        counselor_user_id=row[3],
                        pairing_code=row[4],
                        status=row[5],
                        counselor_pairing_time=row[6],
                        created_at=row[7],
                        updated_at=row[8],
                    )
                return None

    def get_all_pairings(self) -> List[Pairing]:
        query = "SELECT * FROM aits.tb_pairings ORDER BY created_at DESC;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return [
                    Pairing(
                        pairing_id=row[0],
                        client_device_id=row[1],
                        counselor_device_id=row[2],
                        counselor_user_id=row[3],
                        pairing_code=row[4],
                        status=row[5],
                        counselor_pairing_time=row[6],
                        created_at=row[7],
                        updated_at=row[8],
                    ) for row in rows
                ]

    def update_pairing_status(self, pairing_id: int, status: str) -> bool:
        query = """
        UPDATE aits.tb_pairings
        SET status = %s, updated_at = CURRENT_TIMESTAMP
        WHERE pairing_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (status, pairing_id))
                conn.commit()
                return cur.rowcount > 0

    def delete_pairing(self, pairing_id: int) -> bool:
        query = "DELETE FROM aits.tb_pairings WHERE pairing_id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (pairing_id,))
                conn.commit()
                return cur.rowcount > 0

    def drop_table(self):
        query = "DROP TABLE IF EXISTS aits.tb_pairings;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()
