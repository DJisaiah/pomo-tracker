import os
import sqlite3
from datetime import datetime


class LocalDB:
    def __init__(self):
        self._app_data_path = os.getenv("FLET_APP_STORAGE_DATA")
        self._database_path = os.path.join(
            self._app_data_path,
            "database.db"
        )
        self._construct_database()
    
    def _construct_database(self) -> None:
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
                FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
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
            

            # older tables still exist
            subjects_columns_check = "PRAGMA table_info(subjects)"
            cursor.execute(subjects_columns_check)
            subjects_columns = [column[1] for column in cursor.fetchall()]

            if "subject_type" not in subjects_columns:
                add_subject_type_query = "ALTER TABLE subjects ADD subject_type TEXT"
                cursor.execute(add_subject_type_query)
            if "subject_image" not in subjects_columns:
                add_subject_image_query = "ALTER TABLE SUBJECTS ADD subject_image TEXT"
                cursor.execute(add_subject_image_query)

            conn.commit()

    def add_subject(
            self,
            subject_name: str,
            subject_type: str,
            subject_image: str
        ) -> None:
        # add check to see if subject is already in db
        with sqlite3.connect(self._database_path) as conn:
            cursor = conn.cursor()

            add_subject_query = """INSERT INTO 
                subjects (subject_name, subject_type, subject_image)
                VALUES(?, ?, ?)
            """

            cursor.execute(
                add_subject_query,
                (subject_name, subject_type, subject_image)
            )

            conn.commit()
    
    def remove_subject(self, subject_name) -> None:
        with sqlite3.connect(self._database_path) as conn:
            cursor = conn.cursor()

            remove_subject_query = """DELETE FROM subjects WHERE subject_name = ?"""

            cursor.execute(remove_subject_query, (subject_name,))

            conn.commit()
        
    def get_all_subjects(self) -> list[tuple[int, str]]:
        with sqlite3.connect(self._database_path) as conn:
            cursor = conn.cursor()

            get_all_subjects_query = """SELECT id, subject_name from subjects"""

            cursor.execute(get_all_subjects_query)

            all_subjects = cursor.fetchall()
            
            return all_subjects


    def add_session(self, seconds: int, current_subject: str, start_time) -> None:
        with sqlite3.connect(self._database_path) as conn:
            cursor = conn.cursor()
            add_session_query = """INSERT INTO sessions (duration_seconds, start_time, subject_id)
            VALUES (?, ?, ?)
            """

            
            subject_id = cursor.execute("SELECT id FROM subjects WHERE subject_name = ?", 
                                        (current_subject,)).fetchone()[0]

            
            cursor.execute(add_session_query, (seconds, start_time, subject_id))
            
            conn.commit()

    def get_sessions(self,
        number_of_sessions: int, 
        offset: int) -> list[tuple[str, str, int, str, str]]:
        with sqlite3.connect(self._database_path) as conn:
            cursor = conn.cursor()
        get_session_query = """
            SELECT subjects.subject_name,
                sessions.duration_seconds,
                sessions.start_time,
                subjects.subject_type,
                subjects.subject_image
            FROM sessions
            JOIN subjects ON sessions.subject_id = subjects.id
            ORDER BY sessions.id DESC
            LIMIT ?
            OFFSET ?
        """
        cursor.execute(get_session_query, (number_of_sessions, offset))

        sessions = cursor.fetchall()
        return sessions


    def get_day_session_count(self, year, month, day) -> int:
        with sqlite3.connect(self._database_path) as conn:
            cursor = conn.cursor()

            date_pattern = f"{year}-{month}-{day}%"
            get_count_query = """SELECT * FROM sessions WHERE start_time LIKE ?""" 
            
            cursor.execute(get_count_query, (date_pattern,))

            results = cursor.fetchall()

        return len(results)

    def get_all_subject_seconds(self, scale="Y") -> dict[str, int]:
        now = datetime.now()
        year = now.year
        month = f"{now.month:02d}"
        day = f"{now.day:02d}"
        scale = scale.upper()

        # default year case
        year = str(datetime.now().year)
        period_query = """
        WHERE
            strftime('%Y', T1.start_time) = ?
        """
        period_tuple = [year]

        if scale == 'W':
            period_query = """
            WHERE T1.start_time >= date('now', 'weekday 0', '-6 days')
            AND
                T1.start_time <= date('now', 'weekday 0')
            """
            period_tuple = []
        elif scale == 'D':
            period_tuple.extend([month, day])
            period_query += """
            AND
                strftime('%m', T1.start_time) = ?
            AND
                strftime('%d', T1.start_time) = ?
            """
        elif scale == 'M':
            period_tuple.append(month)
            period_query += """
            AND
                strftime('%m', T1.start_time) = ?
            """
        with sqlite3.connect(self._database_path) as conn:
            cursor = conn.cursor()
            subject_sum_query = f"""
            SELECT
                T2.subject_name,
                SUM(T1.duration_seconds) AS total_seconds
            FROM
                sessions AS T1
            JOIN
                subjects AS T2 ON T1.subject_id = T2.id
            {period_query}
            GROUP BY
                T2.subject_name
            """
            cursor.execute(subject_sum_query, tuple(period_tuple))
            results = cursor.fetchall()
            subject_time_dict = dict(results)
        return subject_time_dict

    def get_subjects_info(self) -> list[tuple[int, str, str, str]]:
        with sqlite3.connect(self._database_path) as conn:
            cursor = conn.cursor()

            query = "SELECT * FROM subjects"

            cursor.execute(query)

            results = cursor.fetchall()
        return results

    def update_subject(self, 
        subject_name: str,
        new_subject_name: str,
        new_subject_type: str, 
        new_subject_img: str
        ) -> None:
        with sqlite3.connect(self._database_path) as conn:
            cursor = conn.cursor()

            query = """
                UPDATE subjects
                SET subject_name = ?,
                    subject_type = ?,
                    subject_image = ?
                WHERE subject_name = ?
            """

            cursor.execute(query, (
                new_subject_name,
                new_subject_type,
                new_subject_img,
                subject_name
            ))

            results = cursor.fetchall()
        return results

        
