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
        self._stop_timer: bool = False
        self._isProductive: bool = True
        self._stopwatch: bool = False

    def get_current_time(self) -> str:
        minutes = self._CURRENT_TIME // 60
        seconds = self._CURRENT_TIME % 60
        new_time = (f"{minutes:02}:{seconds:02}")

        return new_time

    def get_current_time_in_seconds(self) -> int:
        return self._CURRENT_TIME
    
    def in_productive_mode(self) -> bool:
        return self._isProductive

    def is_running(self) -> bool:
        return self._timer_running

    def productive_mode(self) -> None:
        self.stop_timer()
        self._isProductive = True
        self._CURRENT_TIME = self._POMODORO * 60
        self._stopwatch = False

    def break_mode(self) -> None:
        self.stop_timer()
        self._isProductive = False
        self._CURRENT_TIME = self._BREAK * 60
        self._stopwatch = False

    def stopwatch_toggle(self) -> None:
        self._stopwatch = True
        self._CURRENT_TIME = 0

    def in_stopwatch_mode(self) -> bool:
        return self._stopwatch

    def get_start_time(self) -> str:
        return self._start_time

    def continue_timer(self) -> None:
        self._stop_timer = False

    async def start_timer(self, update_callback: Callable[[None], [None]]=None) -> None:
        # prevent the user from creating multiple timers
        if self._timer_running and not self._stop_timer:
            return
        else:
            self._timer_running = True
            self._stop_timer = False

        self._start_time = datetime.datetime.now().isoformat(
            timespec='seconds').replace("T", ' ')

        # timer logic
        while self._CURRENT_TIME >= 0:
            if self._stop_timer:
                await asyncio.sleep(1)
                continue
            update_callback()

            await asyncio.sleep(1)

            if self._stopwatch:
                # if timer is paused in stopwatch mode, end session
                if self._stop_timer:
                    return update_callback(True)
                self._CURRENT_TIME += 1
            else:
                self._CURRENT_TIME -= 1
                    
        update_callback(True)

    def stop_timer(self) -> None:
        self._stop_timer = True
        self._timer_running = False

    def increase_timer(self) -> None:
        if self._stopwatch:
            return
        self._CURRENT_TIME += 300

    def decrease_timer(self) -> None:
        if self._CURRENT_TIME - 300 < 0 or self._stopwatch:
            return
        self._CURRENT_TIME -= 300

