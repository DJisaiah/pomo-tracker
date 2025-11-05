import flet as ft
from .TimerControls import TimerControls
from .TimerModeAndSubjectControls import TimerModeAndSubjectControls
from core.timer import Timer
# pom and break need to be fetched from db 
# also need to note linking between the timer page components

class TimerPage:
    def __init__(self, page: ft.Page, db):
        self._page = page
        self._POMODORO = 0.1
        self._BREAK = 5
        self._db = db
        self._timer = Timer(self._POMODORO, self._BREAK)
        self._current_subject = None
        self._controls = TimerControls(self._page, self._timer, self._db, self.get_current_subject)
        self._timer_mode_subject = TimerModeAndSubjectControls(
            self._page,
            self._timer,
            self._db,
            self._controls.set_timer_text,
            self.update_current_subject,
            self.get_current_subject
        )

        
        self._timer_and_controls = ft.Column(controls=[
            self._timer_mode_subject.get_components(),
            self._controls.get_timer_and_inc_dec_buttons(),
            self._controls.get_controls()
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

    def update_current_subject(self, e):
        self._current_subject = e.control.value
    
    def get_current_subject(self):
        print("TIMER CURRENT SBJECT: ", self._current_subject)
        return self._current_subject

    def get_page(self):
        return self._page_layout
    
