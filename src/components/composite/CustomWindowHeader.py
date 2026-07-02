import asyncio

import flet as ft


class CustomWindowHeader(ft.Container):
    def __init__(self, title: str = "POMOTRACKER", height_given: int = 30):
        super().__init__(height=height_given)
        self._title = title
        self._close_button = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_size=16,
            icon_color=ft.Colors.GREY_700,
            hover_color=ft.Colors.RED_500,
            on_click=self._close_app # type: ignore
        )
        self._minimise_button = ft.IconButton(
            icon=ft.Icons.KEYBOARD_ARROW_DOWN,
            icon_size=18,
            icon_color=ft.Colors.GREY_700,
            hover_color=ft.Colors.BLUE_GREY_900,
            on_click=self._minimise_app # type: ignore
        )

    def did_mount(self):
        labels = ft.Row(
            controls=[
                ft.Text(
                    self._title,
                    color=ft.Colors.GREY_700,
                    weight=ft.FontWeight.BOLD,
                    size=10
                ),
                ft.Row(
                    controls=[
                        self._minimise_button,
                        self._close_button
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    spacing=2
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        self.content = ft.WindowDragArea(content=labels)

    def _close_app(self, e: ft.ControlEvent) -> None:
        asyncio.create_task(self.page.window.close()) # type: ignore

    def _minimise_app(self, e: ft.ControlEvent) -> None:
        self.page.window.minimized = True # type: ignore
