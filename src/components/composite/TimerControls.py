from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import flet as ft
from core.enums import StyleTokens

if TYPE_CHECKING:
    from core.PomoUtils import PomoUtils
    from core.Timer import Timer
    from core.TimerPageUtils import TimerActionsAlerts


class TimerControls(ft.Column):
    def __init__(
        self,
        utilities: PomoUtils,
        timer: Timer,
        timer_actions_alerts: TimerActionsAlerts,
    ):
        self._utilities = utilities
        self._timer = timer
        self._timer_actions_alerts = timer_actions_alerts
        super().__init__(alignment=ft.MainAxisAlignment.CENTER, spacing=2)

        # UI components
        self._play_button = ft.Button(
            content=ft.Text("Start", color=ft.Colors.BLACK),
            tooltip="Start/UnPause the timer",
            bgcolor=ft.Colors.GREEN_400,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(
                    side=ft.BorderSide(color=ft.Colors.GREY_700, width=0.1), radius=5
                )
            ),
            on_click=self._start_timer,  # type: ignore
        )

        self._pause_button = ft.Button(
            content=ft.Text("Pause", color=ft.Colors.WHITE_70),
            tooltip="Pause the timer",
            color=ft.Colors.TRANSPARENT,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(
                    side=ft.BorderSide(color=ft.Colors.GREY_700, width=0.1), radius=5
                )
            ),
            on_click=self._pause_timer,  # type: ignore
            disabled=False,
        )

        self._stop_button = ft.Button(
            content=ft.Text("Stop", color=ft.Colors.WHITE_70),
            tooltip="End the timer",
            color=ft.Colors.TRANSPARENT,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(
                    side=ft.BorderSide(color=ft.Colors.GREY_700, width=0.1), radius=5
                )
            ),
            on_click=self._end_timer,  # type: ignore
            disabled=True,
        )

        self._stopwatch_button = ft.Button(
            content=ft.Text("Stopwatch Mode", text_align=ft.TextAlign.CENTER, size=10),
            bgcolor=ft.Colors.BLUE_GREY_900,
            tooltip="Act as a stopwatch and stop when the user wants",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(
                    side=ft.BorderSide(color=ft.Colors.GREY_700, width=0.1), radius=5
                )
            ),
            on_click=self._stopwatch_mode,  # type: ignore
        )

        self._buttons = ft.Row(
            controls=[self._play_button, self._stop_button, self._stopwatch_button],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self._timer_text = ft.Text(
            self._timer.get_current_time(),  # type: ignore
            size=StyleTokens.TIMER_SIZE.value,
            color=ft.Colors.WHITE_70,
        )

        self._increase_button = ft.IconButton(
            icon=ft.Icons.ARROW_UPWARD,
            icon_size=30,
            icon_color=ft.Colors.BLUE_GREY_600,
            tooltip="Increase timer by 5mins",
            on_click=self._increase_timer,  # type: ignore
        )

        self._decrease_button = ft.IconButton(
            icon=ft.Icons.ARROW_DOWNWARD,
            icon_size=30,
            icon_color=ft.Colors.BLUE_GREY_600,
            tooltip="Decrease timer by 5mins",
            on_click=self._decrease_timer,  # type: ignore
        )

        self._timer_and_inc_dec_buttons = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        self._timer_text,
                        ft.Column(
                            controls=[self._increase_button, self._decrease_button]
                        ),
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=80,
        )

        self.controls = [
            self._get_timer_and_inc_dec_buttons(),
            self._get_controls(),
            ft.Container(height=20),
        ]

    def _get_timer_and_inc_dec_buttons(self) -> ft.Row:
        return self._timer_and_inc_dec_buttons

    def _get_controls(self) -> ft.Row:
        return self._buttons

    def set_timer_text(self, time: int | str) -> None:
        if isinstance(time, int):
            self._timer_text.value = f"{time}:00"
        else:
            self._timer_text.value = time  # type: ignore

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

    def _update_page_time(self) -> None:
        new_time = self._timer.get_current_time()
        self.set_timer_text(new_time)
        # self._utilities.update_page() need to check to see if this is actually needed

    def _timer_update_callback(self, done: bool = False) -> None:
        self._update_page_time()
        if done:
            self._timer_actions_alerts.finish()

    async def _start_timer(self, e: ft.ControlEvent) -> None:
        if self._timer_actions_alerts.require_subject():
            return

        if self._timer.is_paused():
            self._timer.unpause()

        self._toggle_start_stop()

        if not self._timer.is_running():
            self._utilities.update_page()
            asyncio.create_task(self._timer.start_timer(self._timer_update_callback))

    def _pause_timer(self, e: ft.ControlEvent) -> None:
        self._timer.stop_timer()
        self._toggle_start_stop()

    def _end_timer(self, e: ft.ControlEvent) -> None:
        self._toggle_start_stop()
        self._timer.end_timer()

    def _stopwatch_mode(self, e: ft.ControlEvent) -> None:
        if self._timer.in_stopwatch_mode():
            self._stopwatch_button.content.value = "Stopwatch Mode"  # type: ignore
            self._timer_actions_alerts.reset()
            return
        else:
            self._stopwatch_button.content.value = "Disable Stopwatch Mode"  # type: ignore
        self._timer.stopwatch_toggle()
        self._update_page_time()
        self._utilities.update_page()

    def _increase_timer(self, e: ft.ControlEvent) -> None:
        if not self._timer.increase_timer():
            self._timer_actions_alerts.upper_timer_limit()
        else:
            self._update_page_time()

    def _decrease_timer(self, e: ft.ControlEvent) -> None:
        if not self._timer.decrease_timer():
            self._timer_actions_alerts.lower_timer_limit()
        else:
            self._update_page_time()
