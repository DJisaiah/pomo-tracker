import flet as ft

from core.enums import StyleTokens


class IslandContainer(ft.Container):
    def __init__(
        self,
        island: ft.Row | ft.Column | ft.Container,
        height_given: int | None = None,
        width_given: int | None = None,
        expand: bool | None = None,
    ):
        super().__init__(
            content=island,
            alignment=ft.Alignment.CENTER,
            padding=ft.Padding.all(1),
            height=height_given,
            width=width_given,
            border_radius=ft.BorderRadius.all(StyleTokens.RADIUS_SMALL.value),
            border=ft.Border.all(
                width=StyleTokens.BORDER_THICKNESS.value,
                color=StyleTokens.BORDER_COLOR.value,
            ),
            expand=expand,
        )
