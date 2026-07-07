from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import flet as ft

if TYPE_CHECKING:
    from core.PomoUtils import PomoUtils
    from core.Timer import Timer
    from core.TimerPageUtils import TimerActionsAlerts


class TimerControls(ft.Row):
    def __init__(
        self,
        utilities: PomoUtils,
        timer: Timer,
        timer_actions_alerts: TimerActionsAlerts,
    ):
        self._utilities = utilities
        self._timer = timer
        self._timer_actions_alerts = timer_actions_alerts
        super().__init__(alignment=ft.MainAxisAlignment.CENTER, spacing=0)

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

        self._timer_text = AbsolutePositionedTime(*self._timer.current_time_list())

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

        self._inc_dec_buttons = ft.Column(
            controls=[
                self._increase_button,
                self._decrease_button,
                ft.Container(height=60),
            ],
            width=50,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.END,
        )

        self.controls = [
            ft.Column(
                controls=[self._timer_text, self._buttons],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=1,
            ),
            self._inc_dec_buttons,
        ]

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

    def update_page_time(self) -> None:
        new_time = self._timer.current_time_list()
        blink = True if self._timer.is_running() else False
        self._timer_text.change_time(new_time[0], new_time[1], blink)
        self._timer_text.update()

    async def _pause_blink(self) -> None:
        while self._timer.is_paused():
            self._timer_text.blink_text()
            await asyncio.sleep(0.5)
        self._timer_text.reset_text()

    def _timer_update_callback(self, done: bool = False) -> None:
        self.update_page_time()
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
            self._utilities.run_task(
                self._timer.start_timer, self._timer_update_callback
            )

    def _pause_timer(self, e: ft.ControlEvent) -> None:
        self._timer.stop_timer()
        self._toggle_start_stop()
        self._utilities.run_task(self._pause_blink)  # type: ignore

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
        self.update_page_time()
        self._utilities.update_page()

    def _increase_timer(self, e: ft.ControlEvent) -> None:
        if not self._timer.increase_timer():
            self._timer_actions_alerts.upper_timer_limit()
        else:
            self.update_page_time()

    def _decrease_timer(self, e: ft.ControlEvent) -> None:
        if not self._timer.decrease_timer():
            self._timer_actions_alerts.lower_timer_limit()
        else:
            self.update_page_time()


class AbsolutePositionedTime(ft.Row):
    """
    positions time absolutely for a text size of 130
    this will likely be scaled later for responsiveness but for now this is it

    allows for blinking of divisor
    """

    def __init__(self, minute: int, seconds: int):
        super().__init__(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=-20,
            width=430,
            height=180,
            tight=True,
        )
        self._blinked = True

        self._minute = ft.Text(
            f"{minute:02d}",
            size=130,
            width=200,
            color=ft.Colors.WHITE_70,
            text_align=ft.TextAlign.CENTER,
            data=True,  # for blinking
        )
        self._divisor = ft.Text(
            ":",
            size=130,
            width=30,
            color=ft.Colors.WHITE_70,
            text_align=ft.TextAlign.CENTER,
        )

        self._seconds = ft.Text(
            f"{seconds:02d}",
            size=130,
            width=200,
            color=ft.Colors.WHITE_70,
            text_align=ft.TextAlign.CENTER,
        )

        self.controls = [self._minute, self._divisor, self._seconds]

    def change_time(self, minute: int, seconds: int, blink: bool = False) -> None:
        self._minute.value = f"{minute:02d}"
        self._seconds.value = f"{seconds:02d}"
        if minute >= 100:
            self._minute.width = 260  # type: ignore
        else:
            self._minute.width = 200  # type: ignore

        # divisor blink
        if blink:
            if self._divisor.color == ft.Colors.WHITE_70:
                self._divisor.color = ft.Colors.GREEN_200
            else:
                self._divisor.color = ft.Colors.WHITE_70

    def blink_text(self):
        color = ft.Colors.TRANSPARENT if self._blinked else ft.Colors.WHITE_70
        self._minute.color = color
        self._seconds.color = color
        self._blinked = not self._blinked
        self.update()

    def reset_text(self):
        self._minute.color = ft.Colors.WHITE_70
        self._seconds.color = ft.Colors.WHITE_70
        self.update()
