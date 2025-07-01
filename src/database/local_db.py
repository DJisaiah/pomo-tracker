import os
import sqlite3


class LocalDB:
    def __init__(self):
        self._app_data_path = os.getenv("FLET_APP_STORAGE_DATA")_
        self._database_path = os.path.join(
            self._app_data_path,
            "database.db"
        )
        self._construct_database()
    
    def _construct_database(self):
        with sqlite3.connect(self._database_path) as conn:
            cursor = conn.cursor()

            subjects_table = """CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY,
                subject_name TEXT NOT NULL UNIQUE,
            );
            """

            sessions_table = """CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                duration_seconds INTEGER NOT NULL,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                subject_id INTEGER NOT NULL,
                FOREIGN KEY (subject_id) REFERENCES subjects(id)
            );
            """

            settings_table = """CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY,
                pomodoro_duration_seconds INTEGER NOT NULL DEFAULT 1500,
                break_duration_seconds INTEGER NOT NULL DEFAULT 300,
                theme TEXT DEFAULT black_green
            );
            """

