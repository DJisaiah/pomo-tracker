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
        super().__init__(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=1,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self._play_button = ft.Button(
            content=ft.Text("Start", color=ft.Colors.BLACK, weight=ft.FontWeight.W_900),
            tooltip="Start/UnPause the timer",
            bgcolor="#7ED957",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(
                    side=ft.BorderSide(color=ft.Colors.GREY_700, width=0.1), radius=10
                )
            ),
            on_click=self._start_timer,  # type: ignore
        )

        self._pause_button = ft.Button(
            content=ft.Text(
                "Pause", color=ft.Colors.WHITE_70, weight=ft.FontWeight.W_900
            ),
            tooltip="Pause the timer",
            color=ft.Colors.TRANSPARENT,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(
                    side=ft.BorderSide(color=ft.Colors.GREY_700, width=2), radius=10
                )
            ),
            on_click=self._pause_timer,  # type: ignore
            disabled=False,
        )

        self._play_pause_button = ft.AnimatedSwitcher(
            content=self._play_button,
            duration=200,
            reverse_duration=200,
        )

        self._stop_button = ft.Button(
            content=ft.Text("Stop", color=ft.Colors.RED, weight=ft.FontWeight.W_900),
            tooltip="End the timer",
            color=ft.Colors.TRANSPARENT,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(
                    side=ft.BorderSide(color=ft.Colors.GREY_700, width=2), radius=10
                )
            ),
            on_click=self._end_timer,  # type: ignore
            disabled=True,
        )

        self._stopwatch_button = ft.Button(
            content=ft.Text("Stopwatch", text_align=ft.TextAlign.CENTER),
            bgcolor=ft.Colors.TRANSPARENT,
            tooltip="Act as a stopwatch and stop when the user wants",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(
                    side=ft.BorderSide(color=ft.Colors.GREY_700, width=2), radius=10
                )
            ),
            on_click=self._stopwatch_mode,  # type: ignore
        )

        self._timer_text = AnimatedTime(*self._timer.current_time_list())

        self._increase_button = ft.IconButton(
            icon=ft.Icons.ADD_CIRCLE_OUTLINE,
            icon_color=ft.Colors.GREY_400,
            tooltip="Increase timer by 5mins",
            on_click=self._increase_timer,  # type: ignore
        )

        self._decrease_button = ft.IconButton(
            icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
            icon_color=ft.Colors.GREY_400,
            tooltip="Decrease timer by 5mins",
            on_click=self._decrease_timer,  # type: ignore
        )

        if self._utilities.mobile_mode():
            self._buttons = ft.Row(
                controls=[
                    self._stop_button,
                    self._play_pause_button,
                    self._stopwatch_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )

            self.controls = [
                self._timer_text,
                ft.Row(
                    controls=[self._decrease_button, self._increase_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                self._buttons,
            ]
            self.spacing = -1
            self._timer_text.height = 100
            self._timer_text.set_size(90)

        else:
            self._buttons = ft.Row(
                controls=[
                    self._decrease_button,
                    self._stop_button,
                    self._play_pause_button,
                    self._stopwatch_button,
                    self._increase_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )

            self.controls = [
                self._timer_text,
                self._buttons,
            ]

    def reset_start_stop(self) -> None:
        self._play_button.disabled = False
        self._play_button.icon_color = ft.Colors.GREEN_300
        self._stop_button.disabled = True
        self._stop_button.icon_color = ft.Colors.GREY_500
        self._play_pause_button.content = self._play_button

    def _toggle_start_stop(self) -> None:
        if self._timer.is_paused():
            self._play_pause_button.content = self._play_button
        else:
            self._play_pause_button.content = self._pause_button
            self._stop_button.disabled = False
            self._stop_button.icon_color = ft.Colors.GREEN_300
        self._play_pause_button.update()

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
            self._stopwatch_button.update()
            self._timer_actions_alerts.reset()
            self._timer.productive_mode()
            self.update_page_time()
            return
        self._stopwatch_button.content.value = "Disable Stopwatch Mode"  # type: ignore
        self._timer.stopwatch_toggle()
        self._stopwatch_button.update()
        self.update_page_time()
        self.reset_start_stop()

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


class AnimatedTime(ft.Row):
    """
    allows for blinking of divisor and time
    """

    def __init__(self, minute: int, seconds: int):
        super().__init__(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=-20,
            # width=430,
            # height=170,
            tight=True,
        )
        self._blinked = True

        self._minute = ft.Text(
            f"{minute:02d}",
            font_family="JetBrains Mono",
            size=130,
            color=ft.Colors.WHITE_70,
            text_align=ft.TextAlign.CENTER,
            data=True,  # for blinking
        )
        self._divisor = ft.Text(
            ":",
            font_family="JetBrains Mono",
            size=130,
            color=ft.Colors.WHITE_70,
            text_align=ft.TextAlign.CENTER,
        )

        self._seconds = ft.Text(
            f"{seconds:02d}",
            font_family="JetBrains Mono",
            size=130,
            color=ft.Colors.WHITE_70,
            text_align=ft.TextAlign.CENTER,
        )

        self.controls = [self._minute, self._divisor, self._seconds]

    def set_size(self, size: int) -> None:
        self._minute.size = size
        self._divisor.size = size
        self._seconds.size = size

    def change_time(self, minute: int, seconds: int, blink: bool = False) -> None:
        self._minute.value = f"{minute:02d}"
        self._seconds.value = f"{seconds:02d}"
        # divisor blink
        if blink:
            if self._divisor.color == ft.Colors.WHITE_70:
                self._divisor.color = StyleTokens.POMO_GREEN.value
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
