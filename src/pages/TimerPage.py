from __future__ import annotations

from typing import TYPE_CHECKING

import flet as ft

from components.base.IslandContainer import IslandContainer
from core.TimerPageUtils import TimerPageUtils

if TYPE_CHECKING:
    from components.composite.TimerControls import TimerControls
    from components.composite.TimerModePanel import TimerModePanel
    from core.PomoUtils import PomoUtils
    from core.TimerPageUtils import SubjectPicker


class TimerPage(ft.Column):
    def __init__(self, utils: PomoUtils):
        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            expand=True,
        )

        # page components
        self._timer_page_utils = TimerPageUtils(utils)
        self._subject_picker: SubjectPicker = (
            self._timer_page_utils.get_subject_picker()
        )
        self._timer_mode_panel: TimerModePanel = (
            self._timer_page_utils.get_timer_mode_panel()
        )
        self._timer_controls: TimerControls = (
            self._timer_page_utils.get_timer_controls()
        )

        self.controls = [
            IslandContainer(island=self._subject_picker),
            IslandContainer(
                island=ft.Column(
                    controls=[self._timer_mode_panel, self._timer_controls],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
            ft.Container(expand=True),
        ]
        self.alignment = ft.MainAxisAlignment.CENTER

    def did_mount(self):
        # if any missing subject data summon dialog for each
        self._timer_page_utils._check_subjects()
