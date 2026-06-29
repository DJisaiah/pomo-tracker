from __future__ import annotations
from typing import Callable, TYPE_CHECKING
import flet as ft
from .TimerControls import TimerControls
from .TimerModeAndSubjectControls import TimerModeAndSubjectControls
import pages.DesignLanguage as ui
from core.timer import Timer

if TYPE_CHECKING:
    from core.PomoUtilities import PomoUtilities
    from database.local_db import LocalDB

class TimerPage:
    class TimerPageUtilities:
        def __init__(self, timer_page: TimerPage, utilities: PomoUtilities):
            self._timer_page: TimerPage = timer_page
            self._utilities: PomoUtilities = utilities
            # section to fetch settings pomo and break length
            self._POMODORO: int = 25
            self._BREAK: int = 5
            self._db: LocalDB = self._utilities.get_db()
            self._timer: Timer = Timer(self._POMODORO, self._BREAK)
            self._current_subject: str = None


        # check subjects and make sure all info is there
        def _check_subjects(self) -> None:
            subjects_info = self._db.get_subjects_info()
            for subject in subjects_info:
                subject_id, subject_name, subject_type, subject_image = subject
                if not subject_type or not subject_image:
                    (self._timer_page.
                    _timer_mode_subject.
                    _edit_subject(None, subject_name)
                    )
                    self._utilities.alert_user(
                        "Missing Subject Data!",
                        f"You're missing subject type/image for \n{subject_name}!"
                    )

        def get_timer(self) -> Timer:
            return self._timer

        def set_timer_text(self, text: str) -> Callable[[str], [None]]:
            self._timer_page._controls.set_timer_text(text)

        def update_current_subject(self, e: ft.ControlEvent) -> None:
            print("current subject updtyed")
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

        def reset_timer(self) -> None:
            self._timer_page._timer_mode_subject._productive_toggle()

        def get_pomodoro_length(self):
            return self._POMODORO
            
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

