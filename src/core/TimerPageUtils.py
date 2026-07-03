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
        self._timer: Timer = Timer(self._pomodoro, self._break, self._state_listener)
        self._timer_actions_alerts = TimerActionsAlerts(
            self._upper_timer_limit,
            self._lower_timer_limit,
            self._require_subject,
            self._timer_finished,
            self._reset_timer,
        )
        self._timer_mode_panel: TimerModePanel = TimerModePanel(
            utilities, self._timer, self._reset_timer_buttons, self._subject_actions
        )
        self._timer_controls: TimerControls = TimerControls(
            utilities, self._timer, self._timer_actions_alerts
        )

    def _state_listener(self) -> None:
        timer_payload = TimerRPCPayload(
            self._subject_utils.get_current_subject(),
            self._subject_utils.get_current_subject_type(),
            self._timer.in_productive_mode(),
            self._timer.in_stopwatch_mode(),
            self._timer.get_current_time(),
            self._timer.get_current_time_in_seconds(),
            self._timer.is_paused(),
            self._timer.is_running(),
            self._timer.timer_ended(),
        )
        self._RPC.timer_state_listener(timer_payload)

    def get_timer_mode_panel(self) -> TimerModePanel:
        return self._timer_mode_panel

    def get_timer_controls(self) -> TimerControls:
        return self._timer_controls

    # check subjects and make sure all info is there
    def _check_subjects(self) -> None:
        self._subject_actions.check_subjects()
        self._timer_mode_panel._update_menu()

    def _set_timer_text(self, time: int) -> None:
        formatted_time = f"{self._timer.get_pomo_length()}:00"
        self._timer_controls.set_timer_text(formatted_time)

    def _require_subject(self) -> bool:
        if (
            self._subject_utils.get_current_subject() == ""
            and self._timer.in_productive_mode()
        ):
            self._utilities.alert_user(
                "No Subject Selected",
                "Please select or create a subject before starting a timer.",
            )
            return True
        return False

    def _timer_finished(self) -> None:
        current_subject: str = self._subject_utils.get_current_subject()
        if self._timer.in_stopwatch_mode() and self._timer.in_productive_mode():
            self._db.add_session(
                self._timer.get_time_elapsed_in_seconds(),
                current_subject,
                self._timer.get_start_time(),
            )
        elif self._timer.in_productive_mode():
            self._db.add_session(
                self._timer.get_time_elapsed_in_seconds(),
                current_subject,
                self._timer.get_start_time(),
            )
        self._utilities.play_finished()
        self._utilities.simple_alert("Timer Finished!")
        self._reset_timer()

    def _upper_timer_limit(self) -> None:
        if self._timer.in_productive_mode():
            self._utilities.alert_user("Pomo Length Cannot Reach 8hrs", "Take breaks.")
        elif self._timer.in_stopwatch_mode():
            self._utilities.alert_user(
                "Good try!", "you cannot increase timers in stopwatch mode"
            )
        else:
            self._utilities.alert_user(
                "Rest.", "With a break this long just close the app"
            )

    def _lower_timer_limit(self) -> None:
        if self._timer.in_stopwatch_mode():
            self._utilities.alert_user(
                "Good try!", "you cannot increase timers in stopwatch mode"
            )
        else:
            self._utilities.alert_user(
                "Minimum Timer Length", "timers must be greater than 0"
            )

    def _toggle_start_stop(self) -> None:
        self._timer_controls._toggle_start_stop()

    def _reset_timer(self) -> None:
        self._timer_mode_panel._productive_toggle()

    def _reset_timer_buttons(self, productive: bool) -> None:
        self._toggle_start_stop()
        time = self._pomodoro if productive else self._break
        self._set_timer_text(time)


@dataclass
class TimerRPCPayload:
    subject_name: str
    subject_type: str
    productive: bool
    stopwatch: bool
    current_time: str
    current_time_seconds: int
    paused: bool
    running: bool
    ended: bool


@dataclass
class TimerActionsAlerts:
    upper_timer_limit: Callable[[], None]
    lower_timer_limit: Callable[[], None]
    require_subject: Callable[[], bool]
    finish: Callable[[], None]
    reset: Callable[[], None]
