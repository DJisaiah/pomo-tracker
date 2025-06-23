import asyncio
import flet as ft

class Timer:
    def __init__(self, page: ft.Page):
        self.page = page
        self._POMODORO = 25
        self._CURRENT_TIME = pomodoro * 60
        self._timer_running = False

    async def start_timer(self, e):
        # prevent the user from creating multiple timers
        if self._timer_running:
            return
        else:
            self._timer_running = True

        # store button and disable on click
        start_button = buttons.controls[0]
        timer = timer_text.controls[0]
        start_button.disabled = True

        # timer logic
        while self._CURRENT_TIME >= 0:
            minutes = self._CURRENT_TIME // 60
            seconds = self._CURRENT_TIME % 60
            timer.value = f"{minutes:02d}:{seconds:02d}"
            self.page.update()
            await asyncio.sleep(1)
            self._CURRENT_TIME -= 1
        timer.value = "Timer Finished!"
