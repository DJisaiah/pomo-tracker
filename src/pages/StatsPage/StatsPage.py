import flet as ft 
from database.local_db import LocalDB
from .HeatMapGrid import HeatMapGrid

class StatsPage:
    def __init__(self, page: ft.Page) -> None:
        self._page = page
        self._db = LocalDB()
        self._heatmap = HeatMapGrid()
        self._page_layout = ft.Column(controls=[
            ft.Container(),
            self._heatmap.get_heatmap()
        ])

    def get_page(self):
        return self._page_layout