from sqlite3 import Connection, Cursor
from typing import Tuple
from webbrowser import get


class EpisodeDatabase:
    def __init__(self, db: Cursor, database_connection: Connection):
        self.db: Cursor = db
        self.cashe_lifetime = 6
        self.conn = database_connection
        self.table_name = "episodes"
        self.db.execute(
            f"""
                CREATE TABLE IF NOT EXISTS {self.table_name}(
                    id INT PRIMARY KEY,
                    url VARCHAR(255) NOT NULL,
                    public_id VARCHAR(255) NOT NULL UNIQUE,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
                """
        )

    def set_casched_episode(self, url: str, public_id: str) -> None:
        self.db.execute(
            f"""
            INSERT OR IGNORE INTO {self.table_name}(url, public_id)
                            VALUES(?, ?)
        """,
            (
                url,
                public_id,
            ),
        )
        self.conn.commit()

    def get_casched_episode(self, public_id) -> Tuple[str, str]:
        res = self.db.execute(
            f"SELECT public_id, url FROM {self.table_name} WHERE public_id=?",
            (public_id,),
        )
        return res.fetchone()

    def clear_cashe(self) -> None:
        self.db.execute(
            f"""
            DELETE FROM {self.table_name} 
            WHERE datetime(timestamp, '+{self.cashe_lifetime} Hour') <= datetime('now')
            """,
        )
        self.conn.commit()
