from __future__ import annotations
from typing import Callable, TYPE_CHECKING
import flet as ft
import asyncio
import time

if TYPE_CHECKING:
    from TimerPage.TimerPage import TimerPage


class TimerControls:
    def __init__(self, utilities: TimerPage.TimerPageUtilities):
        self._tp_utilities: TimerPage.TimerPageUtilities = utilities
        self._utilities: PomoUtilities = self._tp_utilities.get_utilities()
        self._timer: Timer = self._tp_utilities.get_timer()
        self._get_current_subject: Callable[[None], [str]] = self._tp_utilities.get_current_subject
        self._db: LocalDB = self._tp_utilities.get_utilities().get_db()
        self._get_pomodoro_length: Callable[[None], [int]] = self._tp_utilities.get_pomodoro_length

        # controls
        self._play_button = ft.IconButton(
            icon=ft.Icons.PLAY_CIRCLE,
            icon_size=90,
            tooltip="Start the timer",
            icon_color=ft.Colors.GREEN_300,
            on_click=self._start_timer,
        )

        self._pause_button = ft.IconButton(
            icon=ft.Icons.PAUSE_CIRCLE,
            icon_size=90,
            icon_color=ft.Colors.GREEN_300,
            tooltip="Pause the timer",
            on_click=self._pause_timer,
            disabled=False
        )

        self._stop_button = ft.IconButton(
            icon=ft.Icons.STOP_CIRCLE,
            icon_size=90,
            icon_color=ft.Colors.GREY_500,
            tooltip="End the timer",
            on_click=self._end_timer,
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
        spacing=80,
        )

    def get_timer_and_inc_dec_buttons(self) -> ft.Row:
        return self._timer_and_inc_dec_buttons

    def get_controls(self) -> ft.Row:
        return self._buttons

    def _timer_finished(self) -> None:
        if not self._timer.in_productive_mode():
            return
        if self._timer.in_stopwatch_mode() and self._timer.in_productive_mode():
            self._db.add_session(
                self._timer.get_current_time_in_seconds() / 60,
                self._get_current_subject(),
                self._timer.get_start_time()
                )
            self._utilities.play_sound(
                "audio/finished_sound.mp3",
                True,
                0.2
            )
        elif self._timer.in_productive_mode():
            self._db.add_session(
                self._get_pomodoro_length(),
                self._get_current_subject(),
                self._timer.get_start_time()
            )
            self._utilities.play_sound(
                "audio/finished_sound.mp3",
                True,
                0.2
            )
        else:
            self._utilities.play_sound(
                "audio/break_sound.mp3",
                True,
                0.2
            )
        self._update_page_time(True)
        self._utilities.generic_text_alert("Timer Finished!", "")

    def set_timer_text(self, new_text: str) -> None:
        self._timer_text.value = new_text

    def reset_start_stop(self) -> None:
        self._play_button.disabled = False
        self._play_button.icon_color = ft.Colors.GREEN_300
        self._stop_button.disabled = True
        self._stop_button.icon_color = ft.Colors.GREY_500
        self._buttons.controls[0] = self._play_button
    
    def _toggle_start_stop(self) -> None:
        if self._timer.is_paused():
            self._buttons.controls[0] = self._play_button
        else:
            self._buttons.controls[0] = self._pause_button
            self._stop_button.disabled = False
            self._stop_button.icon_color = ft.Colors.GREEN_300

        self._utilities.update_page()

    def _update_page_time(self, reset=False) -> None:
        if not self._timer.is_running():
            return
        current_subject = self._get_current_subject()
        if not reset:
            new_time = self._timer.get_current_time()
            self.set_timer_text(new_time)
        else:
            default_time_from_db = "25:00"
            new_time = default_time_from_db
            self.set_timer_text(new_time)
        if self._timer.in_productive_mode():
            self._utilities.get_RPC().update_details(f"Studying {self._get_current_subject()}")
            if self._timer.in_stopwatch_mode():
                self._utilities.get_RPC().update_state(f"Stopwatch mode: {self._timer.get_current_time()}")
            else:
                self._utilities.get_RPC().update_state(
                    f"Study time remaining", int(time.time() + self._timer.get_current_time_in_seconds())
                )
        else:
            self._utilities.get_RPC().update_details(
                f"On break from {current_subject if current_subject else "Nothing"}!"
            )
            self._utilities.get_RPC().update_state(
                f"Break time remaining", int(time.time() + self._timer.get_current_time_in_seconds())
            )
        
        self._utilities.update_page()

    def _timer_update_callback(self, done: bool = False) -> None:
        self._update_page_time()
        if done:
            self._utilities.get_RPC().update_details(f"Finished Studying {self._get_current_subject()}")
            self._utilities.get_RPC().update_state("They've yet to go on break?")
            self._timer_finished()
            self.reset_start_stop()

    async def _start_timer(self, e: ft.ControlEvent) -> None:
        if self._get_current_subject() is None and self._timer.in_productive_mode():
            self._utilities.alert_user(
                "No Subject Selected",
                "Please select or create a subject before starting a timer."
            )
            return

        if self._timer.is_paused():
            self._timer.unpause()

        self._toggle_start_stop()


        if not self._timer.is_running():
            self._utilities.update_page()
            asyncio.create_task(self._timer.start_timer(
                self._timer_update_callback
            ))

    def _pause_timer(self, e: ft.ControlEvent) -> None:
        self._timer.stop_timer()
        self._toggle_start_stop() 
        self._utilities.get_RPC().update_state(f"Timer Paused")
        
    def _end_timer(self, e: ft.ControlEvent) -> None:
        self._toggle_start_stop()
        self._timer.stop_timer()
        self._timer_finished()

    def _stopwatch_mode(self, e: ft.ControlEvent) -> None:
        self._timer.stopwatch_toggle()
        self._update_page_time()
        self._utilities.update_page()

    def _increase_timer(self, e: ft.ControlEvent) -> None:
        self._timer.increase_timer()
        self._tp_utilities.increase_pomo()
        self._update_page_time()

    def _decrease_timer(self, e: ft.ControlEvent) -> None:
        self._timer.decrease_timer()
        self._tp_utilities.decrease_pomo()
        self._update_page_time()
