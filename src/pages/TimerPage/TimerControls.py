import flet as ft
import asyncio

class TimerControls:
    def __init__(self, page, timer, database, get_current_subject):
        self._page = page
        self._timer = timer
        self._db = database
        self._POMODORO = 25 # temp
        self._BREAK = 5 # temp
        self._get_current_subject = get_current_subject

        # flags
        self._buttons_toggled = False
        self._timer_started = False

        self._play_button = ft.IconButton(
            icon=ft.Icons.PLAY_CIRCLE,
            icon_size=90,
            tooltip="Start the timer",
            icon_color=ft.Colors.GREEN_300,
            on_click=self._start_timer,
        )

        self._stop_button = ft.IconButton(
            icon=ft.Icons.STOP_CIRCLE,
            icon_size=90,
            icon_color=ft.Colors.GREY_500,
            tooltip="Stop the timer",
            on_click=self._stop_timer,
            disabled=True
        )

        
        self._stopwatch_button = ft.Container(content=
                ft.CircleAvatar(
                    content=ft.Text("Stopwatch \n Mode", text_align=ft.TextAlign.CENTER, size=10),
                    radius=40,
                    bgcolor=ft.Colors.BLUE_GREY_900,
                    tooltip="Act as a stopwatch and stop when the user wants",
                ),
                on_click=self._stopwatch_mode
        )

        self._buttons = ft.Row(controls=[
            self._play_button,
            self._stop_button,
            self._stopwatch_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        )


        self._timer_text = ft.Text(self._timer.get_current_time(), size=150)

        self._increase_button = ft.IconButton(
            icon=ft.Icons.ARROW_UPWARD,
            icon_size = 30,
            icon_color=ft.Colors.BLUE_GREY_600,
            tooltip="Increase timer by 5mins",
            on_click=self._increase_timer
        )

        self._decrease_button = ft.IconButton(
            icon=ft.Icons.ARROW_DOWNWARD,
            icon_size = 30,
            icon_color=ft.Colors.BLUE_GREY_600,
            tooltip="Decrease timer by 5mins",
            on_click=self._decrease_timer
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


    def get_timer_and_inc_dec_buttons(self):
        return self._timer_and_inc_dec_buttons

    def get_controls(self):
        row = ft.Row(controls=[
            self._play_button,
            self._stop_button,
            self._stopwatch_button
        ],
        alignment=ft.MainAxisAlignment.CENTER)

        return row

    def _timer_finished(self):
        if self._timer.in_productive_mode:
            self._db.add_session(self._POMODORO, self._get_current_subject(), self._timer.get_start_time())
        self._update_page_time("Done!")

    def set_timer_text(self, new_text):
        self._timer_text.value = new_text
    
    def _toggle_start_stop(self):

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

    def _update_page_time(self, new_time=None):
        if new_time == None:
            new_time = self._timer.get_current_time()
            self.set_timer_text(new_time)
        else:
            self.set_timer_text(new_time)
        self._page.update()

    def _timer_update_callback(self, done=False):
        self._update_page_time()
        if done:
            self._timer_finished()

    async def _start_timer(self, e):
        self._toggle_start_stop()

        if not self._timer_started:
            asyncio.create_task(self._timer.start_timer(
                self._timer_update_callback))
            self._timer_started = not self._timer_started
        else:
            self._timer.continue_timer()


    def _stop_timer(self, e):
        self._timer.stop_timer()
        self._toggle_start_stop()

    def _stopwatch_mode(self, e):
        self._timer.stopwatch_toggle()
        self._update_page_time("00:00")
        self._page.update()

    def _increase_timer(self, e):
        self._timer.increase_timer()
        self._update_page_time()

    def _decrease_timer(self, e):
        self._timer.decrease_timer()
        self._update_page_time()

