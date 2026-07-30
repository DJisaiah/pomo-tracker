from __future__ import annotations

from typing import TYPE_CHECKING

import flet as ft

from components.base.IslandContainer import IslandContainer
from components.composite.HeatMapGrid import HeatMapGrid
from components.composite.SubjectTrackingGraph import SubjectTrackingGraph

if TYPE_CHECKING:
    from core.DBManager import DBManager
    from core.PomoUtils import PomoUtils


class StatsPage(ft.Column):
    def __init__(self, utilities: PomoUtils):
        super().__init__(
            height=530,
            scroll=ft.ScrollMode.HIDDEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # page components
        self._utilities: PomoUtils = utilities
        self._db: DBManager = utilities.get_db()
        self._heatmap: HeatMapGrid = HeatMapGrid(
            self._db, self._utilities.mobile_mode()
        )
        self._graph_tracker: SubjectTrackingGraph = SubjectTrackingGraph(
            self._db, self._utilities.mobile_mode()
        )

        self.controls = [
            IslandContainer(island=self._heatmap, expand=True),
            IslandContainer(island=self._graph_tracker, expand=True),
        ]

    def refresh(self) -> None:
        if self._db.subject_was_deleted():
            self._heatmap.hard_refresh()
            self._db.reset_subject_deleted_flag()
        else:
            new_count = self._db.get_new_session_count()
            if new_count > 0:
                self._heatmap.soft_refresh(new_count)
                self._db.update_latest_session_id()
        self._utilities.update_page()
