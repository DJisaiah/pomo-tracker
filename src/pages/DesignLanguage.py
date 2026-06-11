from __future__ import annotations
from typing import Callable, List, Dict, TYPE_CHECKING
import flet as ft

def get_island_container(island: ft.Row | ft.Column | ft.Container, height: int = None):
    return ft.Container(
        content=island,
        border_radius=ft.BorderRadius.all(6),
        border=ft.Border.all(
            width=2,
            color=ft.Colors.GREY_900
        )

    )
