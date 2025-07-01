import flet as ft
from core.timer import Timer
from database.local_db import LocalDB as loc_db

class TimerPage:
    def __init__(self, page: ft.Page):
        self._page = page
        self._POMODORO = 25
        self._BREAK = 5
        self._buttons_toggled = False

        self._timer = Timer(self._POMODORO, self._BREAK, self)


        def productive_toggle(e):
            # update colours
            self._study_break_subject_bar.controls[1].selected = False
            self._study_break_subject_bar.controls[1].label.color = ft.Colors.WHITE
            e.control.label.color = ft.Colors.BLACK

            # switch to productive timer
            self._set_timer_text("25:00")
            self._timer.productive_mode()

            self._page.update()

        def break_toggle(e):
            # update colours
            self._study_break_subject_bar.controls[0].selected = False
            self._study_break_subject_bar.controls[0].label.color = ft.Colors.WHITE
            e.control.label.color = ft.Colors.BLACK

            # switch to break timer
            self._set_timer_text("05:00")
            self._timer.break_mode()

            self._page.update()

        self._study_break_subject_bar = ft.Row(controls=[
            ft.Chip(
                label=ft.Text("Productive", color=ft.Colors.BLACK),
                on_select=productive_toggle,
                selected_color=ft.Colors.GREEN_300,
                selected=True,
                show_checkmark=False,
                tooltip="Back to the grind"
            ),
            ft.Chip(
                label=ft.Text("Break", color=ft.Colors.WHITE),
                selected_color=ft.Colors.GREEN_300,
                on_select=break_toggle,
                show_checkmark=False,
                tooltip="Rest for a moment"
            ),
            ft.Dropdown(
                editable=True,
                label="Select a Subject!",
                options=[
                    ft.DropdownOption(
                        key=1,
                        content=ft.Text("Abstract Math"),
                        text="Abstract Math"
                    ),
                    ft.DropdownOption(
                        key=2,
                        content=ft.Text("Pomo-Tracker")
                    )
                ]
            )
            ], 
            alignment=ft.MainAxisAlignment.CENTER
        )

        def stopwatch_mode(e):
            self._timer.stopwatch_toggle()
            self._set_timer_text("00:00")
            self._page.update()

        self._buttons = ft.Row(controls=[
            ft.IconButton(
                icon=ft.Icons.PLAY_CIRCLE,
                icon_size=90,
                tooltip="Start the timer",
                icon_color=ft.Colors.GREEN_300,
                on_click=self._timer.start_timer,
            ),
            ft.IconButton(
                icon=ft.Icons.STOP_CIRCLE,
                icon_size=90,
                icon_color=ft.Colors.GREY_500,
                tooltip="Stop the timer",
                on_click=self._timer.stop_timer,
                disabled=True
                
            ),
            ft.Container(content=
                ft.CircleAvatar(
                    content=ft.Text("Stopwatch \n Mode", text_align=ft.TextAlign.CENTER, size=10),
                    radius=40,
                    bgcolor=ft.Colors.BLUE_GREY_900,
                    tooltip="Act as a stopwatch and stop when the user wants",
                ),
                on_click=stopwatch_mode
            ),
        ], 
        alignment=ft.MainAxisAlignment.CENTER,
        )

        def increase_timer(e):
            self._timer.increase_timer()
            self._page.update()

        def decrease_timer(e):
            self._timer.decrease_timer()
            self._page.update()

        self._timer_and_inc_dec_buttons = ft.Row(controls=[
            ft.Row(controls=[
                ft.Text("25:00", size=150),
                ft.Column(controls=[
                    ft.IconButton(
                        icon=ft.Icons.ARROW_UPWARD,
                        icon_size = 30,
                        icon_color=ft.Colors.BLUE_GREY_600,
                        tooltip="Increase timer by 5mins",
                        on_click=increase_timer
                    ),
                    ft.IconButton(
                        icon=ft.Icons.ARROW_DOWNWARD,
                        icon_size = 30,
                        icon_color=ft.Colors.BLUE_GREY_600,
                        tooltip="Decrease timer by 5mins",
                        on_click=decrease_timer
                    )
                ])
            ])
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=80
        )

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
    
    def _set_timer_text(self, new_text):
        text = self._timer_and_inc_dec_buttons.controls[0].controls[0]
        text.value = new_text
    
    def toggle_start_stop(self):
        play_button = self._buttons.controls[0]
        stop_button = self._buttons.controls[1]

        if self._buttons_toggled:
            play_button.disabled = False
            play_button.icon_color = ft.Colors.GREEN_300
            stop_button.disabled = True
            stop_button.icon_color = ft.Colors.GREY_500
        else:
            play_button.disabled = True
            play_button.icon_color = ft.Colors.GREY_500
            stop_button.disabled = False
            stop_button.icon_color = ft.Colors.GREEN_300

        self._buttons_toggled = not(self._buttons_toggled)

        self._page.update()

    def update_timer_page_time(self, minutes, seconds):
        new_time = (f"{minutes:02d}:{seconds:02d}")
        self._set_timer_text(new_time)
        self._page.update()
    
    def timer_finished(self):
        if self._timer.in_productive_mode:
            loc_db.add(self._POMODORO)
        self._set_timer_text("Done!")