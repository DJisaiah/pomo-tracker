from __future__ import annotations

from typing import TYPE_CHECKING

import flet as ft
from components.composite.HeatMapGrid import HeatMapGrid
from components.composite.SubjectTrackingGraph import SubjectTrackingGraph

if TYPE_CHECKING:
    from core.DBManager import DBManager
    from core.PomoUtils import PomoUtils


class StatsPage(ft.Column):
    def __init__(self, utilities: PomoUtils):
        super().__init__(
            width=600,
            height=500,
            scroll=ft.ScrollMode.HIDDEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # page components
        self._utilities: PomoUtils = utilities
        self._db: DBManager = utilities.get_db()
        self._heatmap: HeatMapGrid = HeatMapGrid(self._db)
        self._graph_tracker: SubjectTrackingGraph = SubjectTrackingGraph(self._db)

        self.controls = [self._heatmap, self._graph_tracker]
