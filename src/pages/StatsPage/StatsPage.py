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
        self._page_layout = ft.Row(controls=[
            ft.Container(),
            ft.Column(controls=[
                ft.Container(),
                self._heatmap.get_heatmap(),
                self._graph_tracker.get_graph(),
            ], scroll=ft.ScrollMode.ALWAYS),
            ft.Container()
        ],
        alignment=ft.MainAxisAlignment.CENTER
        )

    def get_page(self):
        return self._page_layout