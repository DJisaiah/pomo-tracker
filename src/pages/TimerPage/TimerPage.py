import flet as ft
from .TimerControls import TimerControls
from .TimerModeAndSubjectControls import TimerModeAndSubjectControls
from core.timer import Timer
# pom and break need to be fetched from db 
# also need to note linking between the timer page components


# BUSY HERE
# plan to put db in utilities (general)
# put other methods in timerpageutilities
# need to get rid of db dependency in files and finish up timer page utils
# then move onto timer start/stop bug
class TimerPage:
    class TimerPageUtilities:
        def __init__(self, timer_page):
            self._timer_page = timer_page

        def get_current_subject(self):
            return timer_page.get_current_subject()
        
        def get_timer(self):
            return timer_page._timer

        def set_timer_text(self):
            return timer_page._controls.set_timer_text

        def update_current_subject(self, e):
            if e is None:
                timer_page._current_subject = None
                return
            timer_page._current_subject = e.control.value
        
        def get_current_subject(self):
            return timer_page._current_subject
        
        def get_utilities(self):
            return timer_page._utilities


            
    def __init__(self, utilities, db):
        self._utilities = utilities
        self._POMODORO = 25
        self._BREAK = 5
        self._db = db
        self._timer = Timer(self._POMODORO, self._BREAK)
        self._current_subject = None
        self._controls = TimerControls(self._utilities, self._timer, self._db, self.get_current_subject)
        self._timer_mode_subject = TimerModeAndSubjectControls(
            self._utilities,
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


    def get_page(self):
        return self._page_layout
    
