import flet as ft
from core.timer import Timer
from database.local_db import LocalDB

# pom and break need to be fetched from db 
# also need to note linking between the timer page components

class TimerPage:
    def __init__(self, page: ft.Page):
        self._page = page
        self._POMODORO = 25         
        self._BREAK = 5
        self._db = LocalDB()

        self._timer = Timer(self._POMODORO, self._BREAK, self)

        self._timer_and_controls = ft.Column(controls=[
            self._study_break_subject_bar,
            self._timer_and_inc_dec_buttons,
            self._buttons
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=0,
        )

        self._page_layout = ft.Column(controls=[
            ft.Container(),
            self._timer_and_controls
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
        )

    def get_page(self):
        return self._page_layout
    
