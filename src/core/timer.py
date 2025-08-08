import asyncio
import datetime

class Timer:
    def __init__(self, POMODORO, BREAK):
        self._POMODORO = POMODORO
        self._BREAK = BREAK
        self._CURRENT_TIME = self._POMODORO * 60
        self._timer_running = False
        self._stop_timer = False
        self._isProductive = True
        self._stopwatch = False
        self._start_time = None

    def get_current_time(self):
        minutes = self._CURRENT_TIME // 60
        seconds = self._CURRENT_TIME % 60
        new_time = (f"{minutes:02d}:{seconds:02d}")

        return new_time
    
    def in_productive_mode(self):
        return self._isProductive

    def productive_mode(self):
        self._isProductive = True
        self._CURRENT_TIME = self._POMODORO * 60

    def break_mode(self):
        self._isProductive = False
        self._CURRENT_TIME = self._BREAK * 60

    def stopwatch_toggle(self):
        self._stopwatch = True
        self._CURRENT_TIME = 0

    def get_start_time(self):
        return self._start_time

    def continue_timer(self):
        self._stop_timer = False

    async def start_timer(self, update_callback=None):
        # prevent the user from creating multiple timers
        if self._timer_running and not self._stop_timer:
            return
        else:
            self._timer_running = True

        self._start_time = datetime.datetime.now().isoformat(
            timespec='seconds').replace("T", '')

        # timer logic
        while self._CURRENT_TIME >= 0:
            if self._stop_timer:
                await asyncio.sleep(1)
                continue
            update_callback()

            await asyncio.sleep(1)

            if self._stopwatch:
                self._CURRENT_TIME += 1
            else:
                self._CURRENT_TIME -= 1
                    
        update_callback(True)

    def stop_timer(self):
        self._stop_timer = True

    def increase_timer(self):
        if self._stopwatch:
            return
        self._CURRENT_TIME += 300

    def decrease_timer(self):
        if self._CURRENT_TIME - 300 < 0 or self._stopwatch:
            return
        self._CURRENT_TIME -= 300

