import flet as ft 
from database.local_db import LocalDB

class StatsPage:
    def __init__(self, page: ft.Page) -> None:
        self._page = page
        self._db = LocalDB()

        self._last_session = ft.Text(self._db.fetch)