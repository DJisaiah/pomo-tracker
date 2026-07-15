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
            width=600,
            height=400,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )

        # page components
        self._timer_page_utils = TimerPageUtils(utils)
        self._timer_mode_panel: TimerModePanel = (
            self._timer_page_utils.get_timer_mode_panel()
        )
        self._timer_controls: TimerControls = (
            self._timer_page_utils.get_timer_controls()
        )
        self._session_count_text = ft.Text(
            f"Sessions: {self._timer_page_utils.get_session_count()}"
        )
        self._timer_page_utils.set_session_count_listener(self._update_session_count)

        self.controls = [
            ft.Container(),
            self._session_count_text,
            IslandContainer(self._timer_mode_panel, 50, 535),
            IslandContainer(self._timer_controls, 275, 535),
        ]

        # if any missing subject data summon dialog for each
        self._timer_page_utils._check_subjects()

    def _update_session_count(self, count: int) -> None:
        self._session_count_text.value = f"Sessions: {count}"
        self._session_count_text.update()