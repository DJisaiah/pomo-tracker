from __future__ import annotations
from typing import Callable, TYPE_CHECKING
import flet as ft


class FeedCard(ft.Container):
    def __init__(self, subject_name: str, 
        duration: str, start_time: str):
        super().__init__()
        border_radius=ft.BorderRadius.all(6),
        border=ft.Border.all(
            width=2,
            color=ft.Colors.GREY_900
        )

        content=self._get_layout()


    def _get_layout(self):
        ft.Column(
            controls=[
                ft.Row(
                    controls=[time_label] 
                ),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[profile_picture]
                        ),
                        ft.Column(
                            controls=[activity_label]
                        )
                    ]
                ),
                ft.Row(
                    controls=[
                        thumbs_up_button
                        ]
                    )
            ]
        )

    def give_like(self):
        pass

