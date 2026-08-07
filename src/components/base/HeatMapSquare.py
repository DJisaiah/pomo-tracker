from __future__ import annotations

from typing import cast

import flet as ft

from core.enums import StyleTokens


class HeatMapSquare(ft.Container):
    def __init__(self, *, count: int, width: int, height: int, rounding: int):
        self._count = count
        super().__init__(
            bgcolor=self._get_colour(),
            border_radius=ft.BorderRadius.all(rounding),
            width=width,
            height=height,
            on_hover=self._hover,
            alignment=ft.Alignment.CENTER,
            tooltip=ft.Tooltip(
                message=f"Sessions: {count}",
                bgcolor=StyleTokens.CONTAINER_GREY.value,
                text_style=ft.TextStyle(
                    color=ft.Colors.WHITE,
                ),
            ),
        )

    def _hover(self, e: ft.Event[ft.Container]) -> None:
        c = cast(ft.Container, e.control)
        c.border = ft.Border.all(width=2, color=ft.Colors.WHITE) if e.data else None
        c.update()

    def _get_colour(self) -> ft.ColorValue:
        if self._count == 0:
            colour = ft.Colors.GREY_900
        elif self._count == 1:
            colour = "#0e4429"
        elif 1 < self._count <= 3:
            colour = "#006d32"
        elif 3 < self._count <= 5:
            colour = "#26a641"
        elif 5 < self._count <= 8:
            colour = "#39d353"
        else:
            colour = "#7ee787"
        return colour

    def increment(self, amount: int) -> None:
        self._update_square(self._count + amount)

    def set_count(self, count: int) -> None:
        self._update_square(count)

    def _update_square(self, count: int) -> None:
        self._count = count
        self.bgcolor = self._get_colour()
        t = cast(ft.Tooltip, self.tooltip)
        t.message = f"Sessions: {count}"
        self.update()
