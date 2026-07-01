from __future__ import annotations
from typing import TYPE_CHECKING
import flet as ft 
from .HeatMapGrid import HeatMapGrid
from .GraphTracker import GraphTracker

if TYPE_CHECKING:
    from database.local_db import LocalDB
    from core.PomoUtilities import PomoUtilities

class StatsPage:
    def __init__(self, utilities: PomoUtilities):
        self._utilities: PomoUtilities = utilities
        self._db: LocalDB = utilities.get_db()
        self._heatmap: HeatMapGrid = HeatMapGrid(self._db)
        self._graph_tracker: GraphTracker = GraphTracker(self._db, self.refresh_graph)
        self._page_layout = ft.Column(controls=[
                ft.Container(),
                self._heatmap.get_heatmap(),
                ft.Container(),
                self._graph_tracker.get_graph(),
                ft.Container(height=20)
            ],
            width=600,
            height=500,
            scroll=ft.ScrollMode.HIDDEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def refresh_graph(self):
        self._page_layout = ft.Column(controls=[
                ft.Container(),
                self._heatmap.get_heatmap(),
                ft.Container(),
                self._graph_tracker.get_graph(),
                ft.Container(height=20)
            ],
            width=600,
            height=500,
            scroll=ft.ScrollMode.HIDDEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        self._utilities.update_page()

    def get_page(self) -> ft.Column:
        return self._page_layout

