from __future__ import annotations
from typing import Callable
import asyncio
import datetime

class Timer:
    def __init__(self, POMODORO: int, BREAK: int):
        self._POMODORO: int = POMODORO
        self._BREAK: int = BREAK
        self._CURRENT_TIME: int = self._POMODORO * 60
        self._start_time: str = None

        # flags
        self._timer_running: bool = False
        self._timer_stopped: bool = False
        self._isProductive: bool = True
        self._stopwatch: bool = False
        self._timer_ended: bool = False

    def get_pomo_length(self) -> int:
        return self._POMODORO

    def get_break_length(self) -> int:
        return self._BREAK

    def get_current_time(self) -> str:
        minutes = self._CURRENT_TIME // 60
        seconds = self._CURRENT_TIME % 60
        new_time = (f"{minutes:02}:{seconds:02}")

        return new_time

    def get_current_time_in_seconds(self) -> int:
        return self._CURRENT_TIME

    def get_time_elapsed_in_seconds(self) -> int:
        productive_elapsed = self._POMODORO * 60 - self._CURRENT_TIME
        break_elapsed = self._BREAK * 60 - self._CURRENT_TIME
        if self.in_stopwatch_mode:
            return self._CURRENT_TIME
        elif self.in_productive_mode:
            return productive_elapsed if productive_elapsed <= 0 else self._POMODORO * 60
        else:
            return break_elapsed if break_elapsed <= 0 else self._BREAK * 60

    def in_productive_mode(self) -> bool:
        return self._isProductive

    def is_running(self) -> bool:
        return self._timer_running

    def is_paused(self) -> bool:
        return self._timer_stopped

    def productive_mode(self) -> None:
        self.end_timer()
        self._isProductive = True
        self._timer_stopped = False
        self._CURRENT_TIME = self._POMODORO * 60
        self._stopwatch = False

    def break_mode(self) -> None:
        self.end_timer()
        self._isProductive = False
        self._timer_stopped = False
        self._CURRENT_TIME = self._BREAK * 60
        self._stopwatch = False

    def stopwatch_toggle(self) -> None:
        self._stopwatch = True
        self._timer_stopped = False
        self._CURRENT_TIME = 0

    def in_stopwatch_mode(self) -> bool:
        return self._stopwatch

    def get_start_time(self) -> str:
        return self._start_time

    def end_timer(self) -> None:
        self._timer_ended = True
        self._timer_running = False

    def unpause(self):
        self._timer_stopped = False

    async def start_timer(self, update_callback: Callable[[None], [None]]=None) -> None:
        if self._timer_ended and not self._timer_running:
            self._timer_ended = False 

        self._timer_running = True

        self._start_time = datetime.datetime.now().isoformat(
            timespec='seconds').replace("T", ' ')

        # timer logic
        while self._CURRENT_TIME >= 0:
            if self._timer_ended:
                self._timer_ended = False
                update_callback(True) # check this for sending right time back to db
                return
            if self._timer_stopped:
                await asyncio.sleep(1)
                continue
            update_callback()

            await asyncio.sleep(1)

            if self._stopwatch:
                # if timer is paused in stopwatch mode, end session
                if self._timer_ended:
                    return update_callback(True)
                self._CURRENT_TIME += 1
            else:
                self._CURRENT_TIME -= 1
                    
        update_callback(True)

    def stop_timer(self) -> None:
        self._timer_stopped = True

    def increase_timer(self) -> None:
        if self._stopwatch:
            return
        self._CURRENT_TIME += 300

    def decrease_timer(self) -> None:
        if self._CURRENT_TIME - 300 < 0 or self._stopwatch:
            return
        self._CURRENT_TIME -= 300

