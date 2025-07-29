import flet as ft

class TimerControls:
    def __init__(self, page, timer, database):
        self._page = page
        self._timer = timer
        self._db = database
        self._POMODORO = 25 # temp
        self._BREAK = 5 # temp

        # flags
        self._buttons_toggled = False
        self._CURRENT_SUBJECT = None

        self._play_button = ft.IconButton(
            icon=ft.Icons.PLAY_CIRCLE,
            icon_size=90,
            tooltip="Start the timer",
            icon_color=ft.Colors.GREEN_300,
            on_click=self._timer.start_timer,
        )

        self._stop_button = ft.IconButton(
            icon=ft.Icons.STOP_CIRCLE,
            icon_size=90,
            icon_color=ft.Colors.GREY_500,
            tooltip="Stop the timer",
            on_click=self._timer.stop_timer,
            disabled=True
        )

        def stopwatch_mode(e):
            self._timer.stopwatch_toggle()
            self._set_timer_text("00:00")
            self._page.update()
        
        self._stopwatch_button = ft.Container(content=
                ft.CircleAvatar(
                    content=ft.Text("Stopwatch \n Mode", text_align=ft.TextAlign.CENTER, size=10),
                    radius=40,
                    bgcolor=ft.Colors.BLUE_GREY_900,
                    tooltip="Act as a stopwatch and stop when the user wants",
                ),
                on_click=stopwatch_mode
        )

        self._buttons = ft.Row(controls=[
            self._play_button,
            self._stop_button,
            self._stopwatch_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        )

        def increase_timer(e):
            self._timer.increase_timer()
            self._page.update()

        def decrease_timer(e):
            self._timer.decrease_timer()
            self._page.update()

        self._timer_text = ft.Text("25:00", size=150)

        self._increase_button = ft.IconButton(
            icon=ft.Icons.ARROW_UPWARD,
            icon_size = 30,
            icon_color=ft.Colors.BLUE_GREY_600,
            tooltip="Increase timer by 5mins",
            on_click=increase_timer
        )

        self._decrease_button = ft.IconButton(
            icon=ft.Icons.ARROW_DOWNWARD,
            icon_size = 30,
            icon_color=ft.Colors.BLUE_GREY_600,
            tooltip="Decrease timer by 5mins",
            on_click=decrease_timer
        )

        self._timer_and_inc_dec_buttons = ft.Row(controls=[
            ft.Row(controls=[
                self._timer_text,
                ft.Column(controls=[
                    self._increase_button,
                    self._decrease_button
                ])
            ])
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=80
        )

    def _set_timer_text(self, new_text):
        self._timer_text.value = new_text
    
    def toggle_start_stop(self):

        if self._buttons_toggled:
            self._play_button.disabled = False
            self._play_button.icon_color = ft.Colors.GREEN_300
            self._stop_button.disabled = True
            self._stop_button.icon_color = ft.Colors.GREY_500
        else:
            self._play_button.disabled = True
            self._play_button.icon_color = ft.Colors.GREY_500
            self._stop_button.disabled = False
            self._stop_button.icon_color = ft.Colors.GREEN_300

        self._buttons_toggled = not(self._buttons_toggled)

        self._page.update()

    def update_timer_page_time(self, minutes, seconds):
        new_time = (f"{minutes:02d}:{seconds:02d}")
        self._set_timer_text(new_time)
        self._page.update()
    
    def timer_finished(self):
        if self._timer.in_productive_mode:
            self._db.add_session(self._POMODORO, self._CURRENT_SUBJECT, self._timer.get_start_time())
        self._set_timer_text("Done!")