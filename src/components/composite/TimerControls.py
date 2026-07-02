from __future__ import annotations

import asyncio
import time
from typing import TYPE_CHECKING, Callable

import flet as ft

from core.enums import StyleTokens

if TYPE_CHECKING:
    from core.PomoUtils import PomoUtils
    from core.Timer import Timer


class TimerControls:
    def __init__(self,
            utilities: PomoUtils,
            timer: Timer,
            add_session: Callable[[int, str, str], None],
            get_current_subject: Callable[[], str],
            reset_timer: Callable[[], None]
    ):
        self._utilities = utilities
        self._timer = timer
        self._get_current_subject = get_current_subject
        self._add_session = add_session
        self._reset_timer = reset_timer

        # controls
        self._play_button = ft.Button(
            content=ft.Text("Start", color=ft.Colors.BLACK),
            tooltip="Start/UnPause the timer",
            bgcolor=ft.Colors.GREEN_400,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(
                    side=ft.BorderSide(
                        color=ft.Colors.GREY_700,
                        width=0.1
                    ),
                    radius=5
                )
            ),
            on_click=self._start_timer, # type: ignore
        )

        self._pause_button = ft.Button(
            content=ft.Text("Pause", color=ft.Colors.WHITE_70),
            tooltip="Pause the timer",
            color=ft.Colors.TRANSPARENT,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(
                    side=ft.BorderSide(
                        color=ft.Colors.GREY_700,
                        width=0.1
                    ),
                    radius=5
                )
            ),
            on_click=self._pause_timer, # type: ignore
            disabled=False

        )

        self._stop_button = ft.Button(
            content=ft.Text("Stop", color=ft.Colors.WHITE_70),
            tooltip="End the timer",
            color=ft.Colors.TRANSPARENT,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(
                    side=ft.BorderSide(
                        color=ft.Colors.GREY_700,
                        width=0.1
                    ),
                    radius=5
                )
            ),
            on_click=self._end_timer, # type: ignore
            disabled=True
        )

        self._stopwatch_button = ft.Button(
            content=ft.Text("Stopwatch Mode", text_align=ft.TextAlign.CENTER, size=10),
            bgcolor=ft.Colors.BLUE_GREY_900,
            tooltip="Act as a stopwatch and stop when the user wants",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(
                    side=ft.BorderSide(
                        color=ft.Colors.GREY_700,
                        width=0.1
                    ),
                    radius=5
                )
            ),
            on_click=self._stopwatch_mode # type: ignore
        )

        self._buttons = ft.Row(controls=[
            self._play_button,
            self._stop_button,
            self._stopwatch_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        )

        self._timer_text = ft.Text(
            self._timer.get_current_time(), # type: ignore
            size=StyleTokens.TIMER_SIZE.value,
            color=ft.Colors.WHITE_70
        )

        self._increase_button = ft.IconButton(
            icon=ft.Icons.ARROW_UPWARD,
            icon_size = 30,
            icon_color=ft.Colors.BLUE_GREY_600,
            tooltip="Increase timer by 5mins",
            on_click=self._increase_timer # type: ignore
        )

        self._decrease_button = ft.IconButton(
            icon=ft.Icons.ARROW_DOWNWARD,
            icon_size = 30,
            icon_color=ft.Colors.BLUE_GREY_600,
            tooltip="Decrease timer by 5mins",
            on_click=self._decrease_timer # type: ignore
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

    def get_timer_and_buttons(self) -> ft.Column:
        return ft.Column(
            controls=[
                self._get_timer_and_inc_dec_buttons(),
                self._get_controls(),
                ft.Container(height=20)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=2
        )

    def _get_timer_and_inc_dec_buttons(self) -> ft.Row:
        return self._timer_and_inc_dec_buttons

    def _get_controls(self) -> ft.Row:
        return self._buttons

    def _timer_finished(self) -> None:
        if not self._timer.in_productive_mode():
            pass
            #self._update_page_time(True)
        elif self._timer.in_stopwatch_mode() and self._timer.in_productive_mode():
            self._add_session(
                self._timer.get_time_elapsed_in_seconds(),
                self._get_current_subject(),
                self._timer.get_start_time()
            )
        elif self._timer.in_productive_mode():
            self._add_session(
                self._timer.get_time_elapsed_in_seconds(),
                self._get_current_subject(),
                self._timer.get_start_time()
            )
        self._utilities.play_finished()
        self._utilities.simple_alert("Timer Finished!")
        self._reset_timer()

    def set_timer_text(self, time: int | str) -> None:
        if type(time) is int:
            self._timer_text.value = f"{time}:00"
        else:
            self._timer_text.value = time # type: ignore

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

    def _update_page_time(self, reset: bool = False) -> None:
        if not reset:
            new_time = self._timer.get_current_time()
            self.set_timer_text(new_time)
        else:
            self._reset_timer()

        # hard limit of 8hrs for stopwatch
        if (
            self._timer.in_stopwatch_mode()
            and self._timer.get_time_elapsed_in_seconds()
            >= 28800
        ):
            self._timer.end_timer()

        self._utilities.update_page()

    def _timer_update_callback(self, done: bool = False) -> None:
        self._update_page_time()
        if done:
            self._timer_finished()

    async def _start_timer(self, e: ft.ControlEvent) -> None:
        if self._get_current_subject() == "" and self._timer.in_productive_mode():
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

    def _end_timer(self, e: ft.ControlEvent) -> None:
        self._toggle_start_stop()
        self._timer.end_timer()

    def _stopwatch_mode(self, e: ft.ControlEvent) -> None:
        if self._timer.in_stopwatch_mode():
            self._stopwatch_button.content.value = "Stopwatch Mode" # type: ignore
            self._reset_timer()
            return
        else:
            self._stopwatch_button.content.value = "Disable Stopwatch Mode" # type: ignore
        self._timer.stopwatch_toggle()
        self._update_page_time()
        self._utilities.update_page()

    def _increase_timer(self, e: ft.ControlEvent) -> None:
        if self._timer.get_pomo_length() == 480:
            self._utilities.alert_user("Pomo Length Cannot Reach 8hrs", "Take breaks.")
        elif self._timer.get_break_length() == 300:
            self._utilities.simple_alert("With a break this long just close the app")
        else:
            self._timer.increase_timer()
            self._update_page_time()

    def _decrease_timer(self, e: ft.ControlEvent) -> None:
        if self._timer.get_pomo_length() == 0:
            self._utilities.simple_alert("Pomo Length Cannot Go Below 0")
        elif self._timer.get_break_length() == 0:
            self._utilities.simple_alert("Breaks Cannot Go Below 0")
        else:
            self._timer.decrease_timer()
            self._update_page_time()
