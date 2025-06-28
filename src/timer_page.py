import flet as ft
from timer import Timer

class TimerPage:
    def __init__(self, page: ft.Page):
        self._page = page
        self._POMODORO = 25
        self._buttons_toggled = False

        self._study_break_bar = ft.Row(controls=[
            ft.MenuBar(
                expand=False,
                style=ft.MenuStyle(
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.DEEP_PURPLE_ACCENT,
                mouse_cursor={
                ft.ControlState.HOVERED: ft.MouseCursor.WAIT,
                ft.ControlState.DEFAULT: ft.MouseCursor.ZOOM_OUT,
                },
                padding=10,
                side=ft.BorderSide(1, ft.Colors.BLACK)
                ),
                controls=[
                ft.SubmenuButton(
                    content=ft.Text("Productive", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD)
                ),
                ft.SubmenuButton(
                    content=ft.Text("Break", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD)
                )
                ])
            ], 
            alignment=ft.MainAxisAlignment.CENTER
            )

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
                content=ft.Text("Stopwatch Mode", text_align=ft.TextAlign.CENTER),
                radius=40,
                tooltip="Act as a stopwatch and stop when the user wants"
            ),
        ], 
        alignment=ft.MainAxisAlignment.CENTER
        )

        self._timer_and_inc_dec_buttons = ft.Row(controls=[
            ft.Container(),
            ft.Row(controls=[
                ft.Text("25:00", size=150),
                ft.Column(controls=[
                    ft.IconButton(
                        icon=ft.Icons.ARROW_UPWARD,
                        icon_size = 30,
                        tooltip="Increase timer by 5mins"
                    ),
                    ft.IconButton(
                        icon=ft.Icons.ARROW_DOWNWARD,
                        icon_size = 30,
                        tooltip="Decrease timer by 5mins"
                    )
                ])
            ])
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=80
        )

        self._timer_and_controls = ft.Column(controls=[
            self._study_break_bar,
            self._timer_and_inc_dec_buttons,
            self._buttons
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=-30,
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
    
    def set_timer_text(self, new_text):
        self._timer_and_inc_dec_buttons.controls[1].controls[0].value = new_text
    
    def toggle_start_stop(self):
        if self._buttons_toggled:
            self._buttons.controls[0].disabled = False
            self._buttons.controls[1].disabled = True
        else:
            self._buttons.controls[0].disabled = True
            self._buttons.controls[1].disabled = False
        self._buttons_toggled = not(self._buttons_toggled)
