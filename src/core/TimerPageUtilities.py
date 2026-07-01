from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import flet as ft

from core.Timer import Timer

if TYPE_CHECKING:
    from core.PomoUtilities import PomoUtilities
    from core.DatabaseManager import DatabaseManager
    from components.composite.TimerControls import TimerControls
    from components.composite.TimerModePanel import TimerModePanel


class TimerPageUtilities:
    def __init__(
        self,
        utilities: PomoUtilities,
        timer_controls: TimerControls,
        timer_mode_panel: TimerModePanel
    ):
        self._utilities: PomoUtilities = utilities
        self._db: DatabaseManager = self._utilities.get_db()
        self._pomdoro: int
        self._break: int
        self._pomodoro, self._break = self._db.get_session_lengths()
        self._timer: Timer = Timer(self._pomodoro, self._break)
        self._current_subject: str | None = None


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
        return self._pomdoro
