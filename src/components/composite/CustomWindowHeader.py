import asyncio
from typing import cast

import flet as ft


class DesktopWindowHeader(ft.Container):
    def __init__(self, extra_controls: ft.Row | None = None):
        super().__init__(height=30)
        self._close_button = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_size=16,
            icon_color=ft.Colors.GREY_700,
            hover_color=ft.Colors.RED_500,
            on_click=self._close_app,
        )
        self._minimise_button = ft.IconButton(
            icon=ft.Icons.KEYBOARD_ARROW_DOWN,
            icon_size=18,
            icon_color=ft.Colors.GREY_700,
            hover_color=ft.Colors.BLUE_GREY_900,
            on_click=self._minimise_app,
        )

    def did_mount(self):
        labels = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            "Pomo",
                            weight=ft.FontWeight.W_800,
                            size=18,
                            color=ft.Colors.WHITE,
                            font_family="Space Grotesk",
                        ),
                        ft.Text(
                            "-",
                            weight=ft.FontWeight.W_800,
                            size=18,
                            color="#7ED957",
                            font_family="Space Grotesk",
                        ),
                        ft.Text(
                            "Tracker",
                            weight=ft.FontWeight.W_800,
                            size=18,
                            color=ft.Colors.WHITE,
                            font_family="Space Grotesk",
                        ),
                    ],
                    spacing=1,
                ),
                ft.Row(
                    controls=[self._minimise_button, self._close_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    spacing=2,
                ),
                # TODO manage extra controls here
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        self.content = ft.WindowDragArea(content=labels)

    def _close_app(self, e: ft.Event[ft.IconButton]) -> None:
        p = cast(ft.Page, self.page)
        asyncio.create_task(p.window.close())

    def _minimise_app(self, e: ft.Event[ft.IconButton]) -> None:
        p = cast(ft.Page, self.page)
        p.window.minimized = True

    def add_control(self, control: ft.Control):
        pass  # TODO

    def remove_control(self):
        pass  # TODO


class MobileWindowHeader(ft.Container):
    def __init__(self, extra_controls: ft.Row | None = None):
        super().__init__(
            content=ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Pomo",
                                weight=ft.FontWeight.W_800,
                                size=22,
                                color=ft.Colors.WHITE,
                                font_family="Space Grotesk",
                            ),
                            ft.Text(
                                "-",
                                weight=ft.FontWeight.W_800,
                                size=22,
                                color="#7ED957",
                                font_family="Space Grotesk",
                            ),
                            ft.Text(
                                "Tracker",
                                weight=ft.FontWeight.W_800,
                                size=22,
                                color=ft.Colors.WHITE,
                                font_family="Space Grotesk",
                            ),
                        ],
                        spacing=1,
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
        )
        if extra_controls is not None:
            cast(ft.Row, self.content).controls.append(extra_controls)

    def add_control(self, control: ft.Control):
        pass  # TODO

    def remove_control(self):
        pass  # TODO
