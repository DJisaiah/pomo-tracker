from __future__ import annotations

from typing import TYPE_CHECKING

import flet as ft

from components.base.IslandContainer import IslandContainer
from core.TimerPageUtils import TimerPageUtils

if TYPE_CHECKING:
    from components.composite.TimerControls import TimerControls
    from components.composite.TimerModePanel import TimerModePanel
    from core.PomoUtils import PomoUtils


class TimerPage(ft.Column):
    def __init__(self, utils: PomoUtils):
        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            expand=True,
        )

        # page components
        self._timer_page_utils = TimerPageUtils(utils)
        self._timer_mode_panel: TimerModePanel = (
            self._timer_page_utils.get_timer_mode_panel()
        )
        self._timer_controls: TimerControls = (
            self._timer_page_utils.get_timer_controls()
        )

        if utils.mobile_mode():
            self.controls = [
                ft.Container(expand=True),
                IslandContainer(self._timer_controls, None, None, True),
                IslandContainer(self._timer_mode_panel),
            ]
            self.alignment = ft.MainAxisAlignment.END
            self.expand = True
        else:
            self.controls = [
                ft.Container(),
                IslandContainer(self._timer_mode_panel, 50, 535),
                IslandContainer(self._timer_controls, 275, 535),
            ]
            self.width = 600
            self.height = 400

        # if any missing subject data summon dialog for each
        self._timer_page_utils._check_subjects()
