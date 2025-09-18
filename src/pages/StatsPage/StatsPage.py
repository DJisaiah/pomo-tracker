import flet as ft 
from .HeatMapGrid import HeatMapGrid
from .GraphTracker import GraphTracker

class StatsPage:
    def __init__(self, page: ft.Page, db) -> None:
        self._page = page
        self._db = db
        self._heatmap = HeatMapGrid(db)
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