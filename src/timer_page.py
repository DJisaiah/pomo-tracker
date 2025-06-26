import flet as ft
from timer import Timer

class TimerPage:
    def __init__(self, page: ft.Page):
        self._page = page
        self._POMODORO = 25
        self._buttons_toggled = False
        self._timer = Timer(page, self._POMODORO, self)
        self._buttons = ft.Row(controls=[
            ft.IconButton(
                icon=ft.Icons.PLAY_CIRCLE,
                icon_size=90,
                tooltip="Start the timer",
                on_click=self._timer.start_timer,
                disabled_color = ft.Colors.GREY
            ),
            ft.IconButton(
                icon=ft.Icons.STOP_CIRCLE,
                icon_size=90,
                tooltip="Stop the timer",
                on_click=self._timer.stop_timer
            ),
            ft.CircleAvatar(
                content=ft.Text("Custom Timer", text_align=ft.TextAlign.CENTER),
                radius=40,
                tooltip="Set a custom timer"
            ),
            ft.CircleAvatar(
                content=ft.Text("Stopwatch Mode", text_align=ft.TextAlign.CENTER),
                radius=40,
                tooltip="Act as a stopwatch and stop when the user wants"
            ),
        ], alignment=ft.MainAxisAlignment.CENTER)
        self._timer_text = ft.Row(controls=[ft.Text("25:00", size=150)], alignment=ft.MainAxisAlignment.CENTER)

    def get_timer_text(self):
        return self._timer_text
    
    def set_timer_text(self, new_text):
        self._timer_text.controls[0].value = new_text
    
    def get_buttons(self):
       return self._buttons
    
    def toggle_start_stop(self):
        if self._buttons_toggled:
            self._buttons.controls[0].disabled = False
            self._buttons.controls[1].disabled = True
        else:
            self._buttons.controls[0].disabled = True
            self._buttons.controls[1].disabled = False
        self._buttons_toggled = not(self._buttons_toggled)

