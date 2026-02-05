from __future__ import annotations
from typing import Callable, TYPE_CHECKING
import flet as ft
from .TimerControls import TimerControls
from .TimerModeAndSubjectControls import TimerModeAndSubjectControls
from core.timer import Timer

if TYPE_CHECKING:
    from core.PomoUtilities import PomoUtilities
    from database.local_db import LocalDB

class TimerPage:
    class TimerPageUtilities:
        def __init__(self, timer_page: TimerPage, utilities: PomoUtilities):
            self._timer_page: TimerPage = timer_page
            self._utilities: PomoUtilities = utilities
            self._POMODORO: int = 25
            self._BREAK: int = 5
            self._db: LocalDB = self._utilities.get_db()
            self._timer: Timer = Timer(self._POMODORO, self._BREAK)
            self._current_subject: str = None

        def get_timer(self) -> Timer:
            return self._timer

        def set_timer_text(self, text: str) -> Callable[[str], [None]]:
            self._timer_page._controls.set_timer_text(text)

        def update_current_subject(self, e: ft.ControlEvent) -> None:
            if e is None:
                self._current_subject = None
                return
            self._current_subject = e.control.value
        
        def get_current_subject(self) -> str:
            return self._current_subject
        
        def get_utilities(self) -> PomoUtilities:
            return self._utilities

        def toggle_start_stop(self) -> Callable[[None], [None]]:
            self._timer_page._controls._toggle_start_stop()

        def reset_start_stop(self) -> Callable[[None], [None]]:
            self._timer_page._controls.reset_start_stop()

        def increase_pomo(self) -> None:
            self._POMODORO += 5

        def decrease_pomo(self) -> None:
            self._POMODORO -= 5

        def get_pomodoro_length(self):
            return self._POMODORO
            
    def __init__(self, utilities: PomoUtilities):
        self._timer_page_utilities = self.TimerPageUtilities(self, utilities)
        self._controls = TimerControls(self._timer_page_utilities)
        self._timer_mode_subject = TimerModeAndSubjectControls(self._timer_page_utilities)
        self._timer_and_controls_layout = ft.Column(controls=[
            self._timer_mode_subject.get_components(),
            self._controls.get_timer_and_inc_dec_buttons(),
            self._controls.get_controls()
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=0
        )
        self._page_layout = ft.Column(controls=[
            ft.Container(),
            self._timer_and_controls_layout
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
        )

    def get_page(self) -> ft.Column:
        return self._page_layout

