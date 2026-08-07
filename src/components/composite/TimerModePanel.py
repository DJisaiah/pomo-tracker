from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import flet as ft

from components.base.EnhancedCupertinoSlidingSegementedButton import (
    EnhancedCupertinoSlidingSegmentedButton,
)
from core.enums import StyleTokens

if TYPE_CHECKING:
    from core.Timer import Timer


class TimerModePanel(ft.Row):
    def __init__(self, timer: Timer, update_time: Callable[[], None]):
        super().__init__(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self._timer = timer
        self._update_time = update_time

        self._mode_toggles = EnhancedCupertinoSlidingSegmentedButton(
            labels=[
                ft.Text(
                    "Productive",
                    weight=ft.FontWeight.W_400,
                    tooltip="Start Tracking and Update Discord",
                ),
                ft.Text(
                    "Break",
                    weight=ft.FontWeight.W_400,
                    tooltip="Stop Tracking and Update Discord",
                ),
            ],
            colors=[StyleTokens.POMO_GREEN.value, StyleTokens.POMO_ORANGE.value],
            actions=[self._productive, self._break],
        )

        self.controls = [
            self._mode_toggles,
        ]

    def _productive(self):
        self._timer.productive_mode()
        self._update_time()

    def _break(self):
        self._timer.break_mode()
        self._update_time()

    def reset_mode(self):
        self._timer.productive_mode()
        self._mode_toggles.reset()
