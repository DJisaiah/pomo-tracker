from __future__ import annotations

import flet as ft

from core.enums import StyleTokens


class FeedCard(ft.Container):
    def __init__(
        self,
        subject_name: str,
        duration: str,
        start_time: str,
        subject_type: str,
        subject_image: str,
    ):
        super().__init__(
            width=500,
            height=100,
            bgcolor=StyleTokens.CONTAINER_GREY.value,
            clip_behavior=ft.ClipBehavior.NONE,
            padding=ft.Padding.all(StyleTokens.RADIUS_LARGE.value),
            border_radius=ft.BorderRadius.all(StyleTokens.RADIUS_LARGE.value),
            border=ft.Border.all(
                width=StyleTokens.BORDER_THICKNESS.value,
                color=StyleTokens.BORDER_COLOR.value,
            ),
        )

        self.content = self._get_layout(
            subject_name, duration, start_time, subject_type, subject_image
        )

    def _get_layout(
        self,
        subject_name: str,
        duration: str,
        start_time: str,
        subject_type: str,
        subject_image: str,
    ) -> ft.Column:
        username_label = ft.Text(
            "You",  # TODO
            color=ft.Colors.WHITE,
            size=15,
            font_family="Space Grotesk",
        )

        activity_time_label = ft.Text(
            start_time,
            color=ft.Colors.GREY_500,
            weight=ft.FontWeight.W_100,
            size=10,
        )
        activity_picture = ft.Container(
            content=ft.Image(src=f"subject_icons/{subject_image}", height=90), width=175
        )
        activity_label = ft.Column(
            controls=[
                ft.Text(
                    f"{duration} {subject_type}",
                    color=ft.Colors.WHITE_70,
                    weight=ft.FontWeight.W_200,
                    size=11,
                ),
                ft.Text(
                    f"{subject_name}",
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.W_600,
                    size=9 if len(subject_name) >= 27 else 14,
                ),
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        fire_button = ft.IconButton(
            icon=ft.Icons.LOCAL_FIRE_DEPARTMENT_OUTLINED,
            icon_color=ft.Colors.GREY_600,
            icon_size=20,
        )

        layout = ft.Column(
            controls=[
                ft.Row(
                    controls=[username_label, activity_time_label],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    controls=[
                        ft.Column(controls=[activity_picture]),
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        activity_label,
                                        ft.Container(expand=True),
                                        fire_button,
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    vertical_alignment=ft.CrossAxisAlignment.START,
                                )
                            ],
                            expand=True,
                        ),
                    ],
                ),
            ],
            spacing=10,
        )

        return layout

    def give_like(self):
        pass
