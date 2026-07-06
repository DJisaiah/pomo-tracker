from __future__ import annotations

import asyncio
import datetime
from typing import Callable


class Timer:
    def __init__(self, POMODORO: int, BREAK: int, state_listener: Callable[[], None]):
        self._POMODORO: int = POMODORO
        self._pomodoro = POMODORO
        self._BREAK: int = BREAK
        self._break = BREAK
        self._current_time: int = self._POMODORO * 60
        self._start_time: str = ""
        self._state_listener = state_listener
        self._minutes = self._POMODORO
        self._seconds = 0
        self._current_time_list: list[int] = [self._minutes, self._seconds]

        # flags
        self._timer_running: bool = False
        self._timer_stopped: bool = False
        self._isProductive: bool = True
        self._stopwatch: bool = False
        self._timer_ended: bool = False

    def timer_ended(self) -> bool:
        return self._timer_ended

    def get_pomo_length(self) -> int:
        return self._pomodoro

    def get_break_length(self) -> int:
        return self._break

    def current_time_list(self) -> list[int]:
        self._minutes = self._current_time // 60
        self._seconds = self._current_time % 60
        self._current_time_list[0] = self._minutes
        self._current_time_list[1] = self._seconds
        return self._current_time_list

    def get_current_time(self) -> str:
        self._minutes = self._current_time // 60
        self._seconds = self._current_time % 60
        new_time = f"{self._minutes:02}:{self._seconds:02}"
        return new_time

    def get_current_time_in_seconds(self) -> int:
        return self._current_time

    def get_time_elapsed_in_seconds(self) -> int:
        productive_elapsed = self._pomodoro * 60 - self._current_time
        break_elapsed = self._break * 60 - self._current_time
        if self.in_stopwatch_mode():
            return self._current_time
        elif self.in_productive_mode():
            return productive_elapsed if self._current_time > 0 else self._pomodoro * 60
        else:
            return break_elapsed if self._current_time > 0 else self._break * 60

    def get_start_time(self) -> str:
        return self._start_time

    def in_productive_mode(self) -> bool:
        return self._isProductive

    def is_running(self) -> bool:
        return self._timer_running

    def is_paused(self) -> bool:
        return self._timer_stopped and self._timer_running

    def productive_mode(self) -> None:
        self.end_timer()
        self._isProductive = True
        self._timer_stopped = False
        self._current_time = self._POMODORO * 60
        self._pomodoro = self._POMODORO
        self._break = self._BREAK
        self._stopwatch = False

    def break_mode(self) -> None:
        self.end_timer()
        self._isProductive = False
        self._timer_stopped = False
        self._current_time = self._BREAK * 60
        self._pomodoro = self._POMODORO
        self._break = self._BREAK
        self._stopwatch = False

    def stopwatch_toggle(self) -> None:
        self.end_timer()
        self._stopwatch = True
        self._timer_stopped = False
        self._current_time = 0
        self._pomodoro = self._POMODORO
        self._break = self._BREAK
        self._state_listener()

    def in_stopwatch_mode(self) -> bool:
        return self._stopwatch

    def end_timer(self) -> None:
        self._timer_ended = True
        self._timer_running = False
        self._state_listener()

    def unpause(self):
        self._timer_stopped = False
        self._state_listener()

    async def start_timer(
        self, update_callback: Callable[[bool], None] = lambda x: None
    ) -> None:
        """starts a timer

        beyond starting it also holds the timer state in an async loop to
        handle pauses

        Args:
            update_callback: callback to let know when timer is finished (pass True)
            otherwise callback lets know to update time
            (pass nothing which defaults to False)
        """
        if self._timer_ended and not self._timer_running:
            self._timer_ended = False

        self._timer_running = True

        self._start_time = (
            datetime.datetime.now().isoformat(timespec="seconds").replace("T", " ")
        )

        # timer logic
        while self._current_time >= 0:
            if self._timer_ended:
                self._timer_ended = False
                update_callback(True)  # check this for sending right time back to db
                return
            if self._timer_stopped:
                await asyncio.sleep(1)
                continue
            update_callback(False)

            await asyncio.sleep(1)

            if self._stopwatch:
                if self._current_time == 28800:
                    return update_callback(True)
                # if timer is paused in stopwatch mode, end session
                if self._timer_ended:
                    return update_callback(True)
                self._current_time += 1
            else:
                self._current_time -= 1

        update_callback(True)

    def stop_timer(self) -> None:
        self._timer_stopped = True
        self._state_listener()

    def increase_timer(self) -> bool:
        allowed = True
        if self._stopwatch:
            allowed = False
        elif self._isProductive:
            # max productive timer cap of 8hrs
            if self.get_pomo_length() == 480:
                allowed = False
            else:
                self._pomodoro += 5
                self._current_time += 300
        else:
            # max break timer cap of 5hrs
            if self.get_break_length() == 300:
                return False
            else:
                self._break += 5
                self._current_time += 300

        if allowed:
            self._state_listener()
        return allowed

    def decrease_timer(self) -> bool:
        allowed = True
        # timers must be greater than 0
        if self._current_time - 300 <= 0 or self._stopwatch:
            allowed = False
        else:
            self._current_time -= 300

        if self._isProductive:
            self._pomodoro -= 5
        else:
            self._break -= 5

        if allowed:
            self._state_listener()
        return allowed
