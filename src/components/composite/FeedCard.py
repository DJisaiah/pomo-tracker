from __future__ import annotations

import flet as ft


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
            bgcolor=ft.Colors.GREEN_100,
            padding=2,
            border_radius=8,
            border=ft.Border.all(width=3, color=ft.Colors.WHITE_30),
            clip_behavior=ft.ClipBehavior.NONE,
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
        activity_time_label = ft.Text(
            start_time, color=ft.Colors.GREY_900, weight=ft.FontWeight.W_100, size=10
        )
        activity_picture = ft.Container(
            content=ft.Image(src=f"subject_icons/{subject_image}", height=90), width=175
        )
        activity_label = ft.Column(
            controls=[
                ft.Text(
                    f"{duration} {subject_type}",
                    color=ft.Colors.BLACK_87,
                    weight=ft.FontWeight.W_200,
                    size=11,
                ),
                ft.Text(
                    f"{subject_name}",
                    color=ft.Colors.BLACK,
                    weight=ft.FontWeight.W_600,
                    size=9 if len(subject_name) >= 27 else 14,
                ),
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        thumbs_up_button = ft.IconButton(
            icon=ft.Icons.FAVORITE,
            icon_color=ft.Colors.BLACK_12,
        )

        layout = ft.Column(
            controls=[
                ft.Row(
                    controls=[activity_time_label], alignment=ft.MainAxisAlignment.END
                ),
                ft.Row(
                    controls=[
                        ft.Column(controls=[activity_picture]),
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[activity_label, thumbs_up_button],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
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
