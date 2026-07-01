from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import flet as ft

import pages.DesignLanguage as ui
from core.Timer import Timer

from .TimerControls import TimerControls
from .TimerModeAndSubjectControls import TimerModeAndSubjectControls

if TYPE_CHECKING:
    from core.PomoUtilities import PomoUtilities
    from database.LocalDB import LocalDB


class TimerPage:
    def __init__(self, utilities: PomoUtilities):
        self._timer_page_utilities = self.TimerPageUtilities(self, utilities)
        self._controls = TimerControls(self._timer_page_utilities)
        self._timer_mode_subject = TimerModeAndSubjectControls(self._timer_page_utilities)
        self._page_layout = ft.Column(
            controls=[
                ft.Container(),
                ui.get_island_container(self._timer_mode_subject.get_components(), 50, 535),
                ui.get_island_container(self._controls.get_timer_and_buttons(), 275, 535),
            ],
            width=600,
            height=400,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
        self._timer_page_utilities._check_subjects()



    def get_page(self) -> ft.Column:
        return self._page_layout

