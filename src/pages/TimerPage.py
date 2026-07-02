from __future__ import annotations

from typing import TYPE_CHECKING

import flet as ft

from core.TimerPageUtils import TimerPageUtils
from components.base.IslandContainer import IslandContainer



if TYPE_CHECKING:
    from core.PomoUtils import PomoUtils
    from core.DBManager import DBManager
    from components.composite.TimerControls import TimerControls
    from components.composite.TimerModePanel import TimerModePanel


class TimerPage:
    def __init__(self, utils: PomoUtils):
        self._timer_page_utils = TimerPageUtils(utils)
        self._timer_mode_panel = self._timer_page_utils.get_timer_mode_panel()
        self._timer_controls = self._timer_page_utils.get_timer_controls()
        self._page_layout = ft.Column(
            controls=[
                ft.Container(),
                IslandContainer(self._timer_mode_panel, 50, 535),
                IslandContainer(self._timer_controls, 275, 535),
            ],
            width=600,
            height=400,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
        self._timer_page_utils._check_subjects()

    def get_page(self) -> ft.Column:
        return self._page_layout

