import asyncio
import flet as ft

class Timer:
    def __init__(self, page: ft.Page, pomodoro, timer_page):
        self._page = page
        self._timer_page = timer_page
        self._POMODORO = pomodoro
        self._CURRENT_TIME = self._POMODORO * 60
        self._timer_running = False
        self._stop_timer = False

    async def start_timer(self, e):
        # prevent the user from creating multiple timers
        if self._timer_running and not self._stop_timer:
            return
        else:
            self._timer_running = True

        if self._stop_timer:
            self._stop_timer = False

        # store button and disable on click
        self._timer_page.toggle_start_stop()

        # timer logic
        while self._CURRENT_TIME >= 0:
            if self._stop_timer:
                await asyncio.sleep(1)
                continue
            minutes = self._CURRENT_TIME // 60
            seconds = self._CURRENT_TIME % 60
            self._timer_page.set_timer_text(f"{minutes:02d}:{seconds:02d}")
            self._page.update()
            await asyncio.sleep(1)
            self._CURRENT_TIME -= 1
        self._timer_page.set_timer_text("Timer Finished!")

    def stop_timer(self, e):
        self._stop_timer = True
        self._timer_page.toggle_start_stop()
