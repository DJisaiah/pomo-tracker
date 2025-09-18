import os
import sqlite3

class LocalDB:
    def __init__(self):
        self._app_data_path = os.getenv("FLET_APP_STORAGE_DATA")
        self._database_path = os.path.join(
            self._app_data_path,
            "database.db"
        )
        self._construct_database()
    
    def _construct_database(self):
        with sqlite3.connect(self._database_path) as conn:
            cursor = conn.cursor()

            subjects_table = """CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_name TEXT NOT NULL UNIQUE
            );
            """

            sessions_table = """CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                duration_seconds INTEGER NOT NULL,
                start_time TIMESTAMP NOT NULL,
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

            cursor.execute(subjects_table)
            cursor.execute(sessions_table)
            cursor.execute(settings_table)

            conn.commit()

    def add_subject(self, subject_name):
        # add check to see if subject is already in db
        with sqlite3.connect(self._database_path) as conn:
            cursor = conn.cursor()

            add_subject_query = """INSERT INTO subjects (subject_name)
            VALUES(?)
            """

            cursor.execute(add_subject_query, (subject_name,))

            conn.commit()
    
    def remove_subject(self, subject_id):
        with sqlite3.connect(self._database_path) as conn:
            cursor = conn.cursor()

            remove_subject_query = """DELETE FROM subjects WHERE id = ?"""

            cursor.execute(remove_subject_query, (subject_id))

            conn.commit()
        
    def get_all_subjects(self):
        with sqlite3.connect(self._database_path) as conn:
            cursor = conn.cursor()

            get_all_subjects_query = """SELECT id, subject_name from subjects"""

            cursor.execute(get_all_subjects_query)

            all_subjects = cursor.fetchall()
            
            return all_subjects


    def add_session(self, POMODORO, CURRENT_SUBJECT, START_TIME):
        POMODORO = POMODORO * 60
        with sqlite3.connect(self._database_path) as conn:
            cursor = conn.cursor()
            add_session_query = """INSERT INTO sessions (duration_seconds, start_time, subject_id)
            VALUES (?, ?, ?)
            """
            SUBJECT_ID = cursor.execute("SELECT id FROM subjects WHERE subject_name = ?", 
                                        (CURRENT_SUBJECT)).fetchone()

            cursor.execute(add_session_query, (POMODORO, START_TIME, SUBJECT_ID))
            
            conn.commit()


    def get_day_session_count(self, year, month, day):
        with sqlite3.connect(self._database_path) as conn:
            cursor = conn.cursor()

            date_pattern = f"{year}-{month}-{day}%"
            get_count_query = """SELECT * FROM sessions WHERE start_time LIKE ?""" 
            
            cursor.execute(get_count_query, (date_pattern,))

            results = cursor.fetchall()

        return len(results)