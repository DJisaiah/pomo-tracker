import os
import sqlite3
from datetime import datetime


class DBManager:
    def __init__(self) -> None:
        app_env = os.getenv("FLET_APP_STORAGE_DATA")
        self._app_data_path = app_env if app_env is not None else "."
        self._database_path = os.path.join(
            self._app_data_path,
            "database.db"
        )
        self._local = LocalDB(self._database_path)
        # self._remote = RemoteDB()  # cloud sync later

    def add_subject(
        self,
        subject_name: str,
        subject_type: str,
        subject_image: str
    ) -> None:
        self._local.add_subject(subject_name, subject_type, subject_image)

    def remove_subject(self, subject_name: str) -> None:
        self._local.remove_subject(subject_name)

    def get_all_subjects(self) -> list[tuple[int, str]]:
        return self._local.get_all_subjects()

    def add_session(self,
        seconds: int,
        current_subject: str,
        start_time: str
    ) -> None:
        self._local.add_session(seconds, current_subject, start_time)

    def get_sessions(
        self,
        number_of_sessions: int,
        offset: int
    ) -> list[tuple[str, int, str, str, str]]:
        return self._local.get_sessions(number_of_sessions, offset)

    def get_day_session_count(self,
        year: int,
        month: int,
        day: int
    ) -> int:
        return self._local.get_day_session_count(year, month, day)

    def get_all_subject_seconds(self, scale: str = "Y") -> dict[str, int]:
        return self._local.get_all_subject_seconds(scale=scale)

    def get_subjects_info(self) -> list[tuple[int, str, str, str]]:
        return self._local.get_subjects_info()

    def update_subject(
        self,
        subject_name: str,
        new_subject_name: str,
        new_subject_type: str,
        new_subject_img: str
    ) -> None:
        self._local.update_subject(
            subject_name, new_subject_name, new_subject_type, new_subject_img
        )

    def get_session_lengths(self) -> list[int]:
        return self._local.get_session_lengths()

    def change_session_lengths(self, pomo: int, breaks: int) -> None:
        self._local.change_session_lengths(pomo, breaks)


class LocalDB:
    def __init__(self, db_path: str):
        self._database_path = db_path
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

    def remove_subject(self, subject_name: str) -> None:
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

    def add_session(self, seconds: int, current_subject: str, start_time: str) -> None:
        with sqlite3.connect(self._database_path) as conn:
            cursor = conn.cursor()
            add_session_query = """
            INSERT INTO sessions
                (duration_seconds, start_time, subject_id)
                VALUES (?, ?, ?)
            """

            subject_id_query = "SELECT id FROM subjects WHERE subject_name = ?"

            subject_id = cursor.execute(
                subject_id_query,
                (current_subject,)
            ).fetchone()[0]

            cursor.execute(add_session_query, (seconds, start_time, subject_id))
            conn.commit()

    def get_sessions(self,
        number_of_sessions: int,
        offset: int) -> list[tuple[str, int, str, str, str]]:
        """Gets a batch of the latest sessions from the sessions table.

        in order to keep getting disjoint batches you need to
        get the next offset based off your previous limit + offset


        Args:
            number_of_sessions: number of sessions you want
            offset: get the next batch from the nth position (latest)

        Returns:
            a list of a tuples with the subject name, duration in seconds, start time,
            subject type, and subject image
        """
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


    def get_day_session_count(self, year: int, month: int, day: int) -> int:
        with sqlite3.connect(self._database_path) as conn:
            cursor = conn.cursor()

            if month < 10:
                padded_month = f"0{month}"
            else:
                padded_month = month

            if day < 10:
                padded_day = f"0{day}"
            else:
                padded_day = day

            date_pattern = f"{year}-{padded_month}-{padded_day}%"
            get_count_query = """SELECT * FROM sessions WHERE start_time LIKE ?"""
            cursor.execute(get_count_query, (date_pattern,))

            results = cursor.fetchall()

        return len(results)

    def get_all_subject_seconds(self, scale: str = "Y") -> dict[str, int]:
        """gets the total duration of all subjects for a specific period

        filters the data based on the timescale and sums up the
        seconds based on all the sessions

        Args:
            scale: Timeframe filter. Use 'D' for day, 'W' for week, 'M' for month,
            or 'Y' for year. Defaults to "Y".

        Returns:
            returns a dictionary where the key is each subject and the value is the
            summed seconds for your time scale
        """
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
        """gets the data for each column of all subjects in the subject table

        gets you access to all the subject's id, name, type, image

        Returns:
            a list of tuples containing, subject id, name, type, image
        """
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
            conn.commit()

    def get_session_lengths(self) -> list[int]:
        return [25, 5] #TODO

    def change_session_lengths(self, pomo: int, breaks: int) -> None:
        pass #TODO

class RemoteDB:
    pass
