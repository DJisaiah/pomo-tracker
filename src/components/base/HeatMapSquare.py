from __future__ import annotations

import flet as ft


class HeatMapSquare(ft.Container):
    def __init__(self, count: int, width: int, height: int):
        self._count = count
        super().__init__(
            bgcolor=self._get_colour(),
            border_radius=ft.BorderRadius.all(3),
            width=width,
            height=height,
            on_hover=self._hover_text,  # type: ignore
            alignment=ft.Alignment.CENTER,
        )

    def _hover_text(self, e: ft.ControlEvent) -> None:
        square_number = ft.Text(
            str(self._count),
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.WHITE,
            size=10,
            weight=ft.FontWeight.BOLD,
        )
        e.control.content = square_number if e.data is True else None  # type: ignore
        e.control.update()

    def _get_colour(self) -> ft.Colors:
        if self._count == 0:
            colour = ft.Colors.GREY_700
        elif self._count >= 1 and self._count <= 3:
            colour = ft.Colors.GREEN_300
        elif self._count > 3 and self._count < 5:
            colour = ft.Colors.GREEN_500
        elif self._count >= 5 and self._count < 8:
            colour = ft.Colors.GREEN_700
        else:
            colour = ft.Colors.GREEN_900
        return colour


    def increment(self) -> None:
        self._count+=1
        self.bgcolor=self._get_colour()
        self.update()

    def set_count(self, count: int) -> None:
        self._count = count
        self.bgcolor = self._get_colour()
        self.update()
