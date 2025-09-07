import flet as ft 
from database.local_db import LocalDB
from .HeatMapGrid import HeatMapGrid
from .GraphTracker import GraphTracker

class StatsPage:
    def __init__(self, page: ft.Page) -> None:
        self._page = page
        self._db = LocalDB()
        self._heatmap = HeatMapGrid()
        self._graph_tracker = GraphTracker()
        self._page_layout = ft.Column(controls=[
                ft.Container(),
                self._heatmap.get_heatmap(),
                ft.Container(),
                self._graph_tracker.get_graph(),
            ],
            width=600,
            height=500,
            scroll=ft.ScrollMode.HIDDEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )

    def get_page(self):
        return self._page_layout