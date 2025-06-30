import asyncio

class Timer:
    def __init__(self, POMODORO, BREAK, timer_page):
        self._timer_page = timer_page
        self._POMODORO = POMODORO
        self._BREAK = BREAK
        self._CURRENT_TIME = self._POMODORO * 60
        self._timer_running = False
        self._stop_timer = False
        self._isProductive = True
        self._stopwatch = False

    def _update_timer(self):
        minutes = self._CURRENT_TIME // 60
        seconds = self._CURRENT_TIME % 60
        self._timer_page.update_timer_page_time(minutes, seconds)

    def productive_mode(self):
        self._isProductive = True
        self._CURRENT_TIME = self._POMODORO * 60

    def break_mode(self):
        self._isProductive = False
        self._CURRENT_TIME = self._BREAK * 60

    def stopwatch_toggle(self):
        self._stopwatch = True
        self._CURRENT_TIME = 0


    async def start_timer(self, e):
        # prevent the user from creating multiple timers
        if self._timer_running and not self._stop_timer:
            return
        else:
            self._timer_running = True

        if self._stop_timer:
            self._stop_timer = False
            self._timer_page.toggle_start_stop()
            return

        # store button and disable on click
        self._timer_page.toggle_start_stop()

        # timer logic
        while self._CURRENT_TIME >= 0:
            if self._stop_timer:
                await asyncio.sleep(1)
                continue

            self._update_timer()
            await asyncio.sleep(1)

            if self._stopwatch:
                self._CURRENT_TIME += 1
            else:
                self._CURRENT_TIME -= 1

        self._timer_page.timer_finished()

    def stop_timer(self, e):
        self._stop_timer = True
        self._timer_page.toggle_start_stop()

    def increase_timer(self):
        if self._stopwatch:
            return
        self._CURRENT_TIME += 300
        self._update_timer()

    def decrease_timer(self):
        if self._CURRENT_TIME - 300 < 0 or self._stopwatch:
            return
        self._CURRENT_TIME -= 300
        self._update_timer()

