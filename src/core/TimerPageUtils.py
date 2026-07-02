from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from core.SubjectUtils import SubjectUtils
from core.Timer import Timer

if TYPE_CHECKING:
    from components.composite.TimerControls import TimerControls
    from components.composite.TimerModePanel import TimerModePanel
    from core.DBManager import DBManager
    from core.DiscordRPCManager import DiscordRPCManager
    from core.PomoUtils import PomoUtils


class TimerPageUtils:
    def __init__(self, utilities: PomoUtils):
        """utility class for timer page controls and timer page itself

        allows controls access to db, pomoutils, and other inter-control methods

        Args:
            utilities: the shared instance of PomoUtils
        """
        self._utilities: PomoUtils = utilities
        self._db: DBManager = self._utilities.get_db()
        self._RPC: DiscordRPCManager = self._utilities.get_RPC()
        self._pomodoro: int
        self._break: int
        self._pomodoro, self._break = self._db.get_session_lengths()
        self._subject_utils: SubjectUtils = SubjectUtils(utilities)
        self._subject_actions = self._subject_utils.get_actions()
        self._timer: Timer = Timer(
            self._pomodoro,
            self._break,
            self._state_listener
        )
        self._timer_mode_panel: TimerModePanel = TimerModePanel(
            utilities,
            self._timer,
            self.reset_timer_buttons,
            self._subject_actions
        )
        self._timer_controls: TimerControls = TimerControls(
            utilities,
            self._timer,
            self._db.add_session,
            self._subject_actions.current_subject,
            self.reset_timer
        )

        self._timer_payload = TimerRPCPayload(
            self._subject_utils.get_current_subject,
            self._subject_utils.get_current_subject_type,
            self._timer.in_productive_mode,
            self._timer.in_stopwatch_mode,
            self._timer.get_current_time,
            self._timer.get_current_time_in_seconds,
            self._timer.is_paused,
            self._timer.is_running,
            self._timer.timer_ended
        )

    def _state_listener(self) -> None:
        self._RPC.timer_state_listener(self._timer_payload)

    def get_timer_mode_panel(self) -> TimerModePanel:
        return self._timer_mode_panel

    def get_timer_controls(self) -> TimerControls:
        return self._timer_controls

    # check subjects and make sure all info is there
    def _check_subjects(self) -> None:
        self._subject_actions.check_subjects()
        self._timer_mode_panel._update_menu()

    def get_timer(self) -> Timer:
        return self._timer

    def _set_timer_text(self, time: int) -> None:
        formatted_time = f"{self._timer.get_pomo_length()}:00"
        self._timer_controls.set_timer_text(formatted_time)

    def get_utilities(self) -> PomoUtils:
        return self._utilities

    def _toggle_start_stop(self) -> None:
        self._timer_controls._toggle_start_stop()

    def reset_start_stop(self) -> None:
        self._timer_controls.reset_start_stop()

    def reset_timer(self) -> None:
        self._timer_mode_panel._productive_toggle()

    def reset_timer_buttons(self, productive: bool) -> None:
        self._toggle_start_stop()
        time = self._pomodoro if productive else self._break
        self._set_timer_text(time)

    def get_pomodoro_length(self) -> int:
        return self._pomodoro

@dataclass
class TimerRPCPayload:
    subject_name: Callable[[], str]
    subject_type: Callable[[], str]
    productive: Callable[[], bool]
    stopwatch: Callable[[], bool]
    current_time: Callable[[], str]
    current_time_seconds: Callable[[], int]
    paused: Callable[[], bool]
    running: Callable[[], bool]
    ended: Callable[[], bool]
