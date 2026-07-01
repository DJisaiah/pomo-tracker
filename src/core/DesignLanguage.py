from __future__ import annotations
from typing import Callable, List, Dict, TYPE_CHECKING
import flet as ft
import asyncio

def get_island_container(
    island: ft.Row | ft.Column | ft.Container,
    height_given: int = None,
    width_given: int = None
    ):
    return ft.Container(
        content=island,
        alignment=ft.Alignment.CENTER,
        padding=ft.Padding.all(1),
        height=height_given,
        width=width_given,
        border_radius=ft.BorderRadius.all(6),
        border=ft.Border.all(
            width=2,
            color=ft.Colors.GREY_900
        )
    )

def get_window_header(page: ft.Page):

    def close_app(e: ft.ControlEvent):
        asyncio.create_task(page.window.close())

    def minimise_app(e: ft.ControlEvent):
        page.window.minimized = True

    close_button = ft.IconButton(
        icon=ft.Icons.CLOSE,
        icon_size=16,
        icon_color=ft.Colors.GREY_700,
        hover_color=ft.Colors.RED_500,
        on_click=close_app
    )
    
    minimise_button = ft.IconButton(
        icon=ft.Icons.KEYBOARD_ARROW_DOWN,
        icon_size=18,
        icon_color=ft.Colors.GREY_700,
        hover_color=ft.Colors.BLUE_GREY_900,
        on_click=minimise_app
    )

    labels = ft.Row(
        controls=[
            ft.Text(
                "POMOTRACKER",
                color=ft.Colors.GREY_700,
                weight=ft.FontWeight.BOLD,
                size=10
            ),
            ft.Row(
                controls=[
                    minimise_button,
                    close_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=2
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )
    header = ft.WindowDragArea(content=labels)
    return ft.Container(content=header, height=30)

