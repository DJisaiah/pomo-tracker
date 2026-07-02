from typing import Callable

import flet as ft

from components.base.ImagePicker import ImagePicker
from core.enums import SubjectIcons


class SubjectEditor(ft.AlertDialog):
    def __init__(
        self,
        click_action: Callable[[ft.ControlEvent, list[str]], None],
        initial_subject: str = ""
        ):
        """prompt the user for a subject name, subject type, subject image
        performs a callback action based on that data

        upon submission the data is passed as a list (in the order prompted)
        as parameters to the callback with the intial subject (first)

        Args:
            click_action: callback function that accepts a list of strings as params
            initial_subject: str subject name to prepopulate form
        """
        super().__init__()
        self.bgcolor=ft.Colors.BLACK
        self.alignment=ft.Alignment.CENTER
        self.content_padding = ft.Padding(bottom=30, top=30)
        self.shape=ft.RoundedRectangleBorder(
            radius=10,
            side=ft.BorderSide(color=ft.Colors.GREY_700, width=2)
        )

        self.actions = [
            ft.TextButton(
                content=ft.Text("Cool.", color=ft.Colors.GREEN_700),
                on_click=lambda e: self._send_form_data_back(
                    click_action,
                    initial_subject
                )
            )
        ]

        self.content = ft.Column(
            controls=[
                self.get_subject_field(initial_subject),
                self.get_subject_type_text(),
                self.get_subject_type_toggles(),
                ImagePicker(
                    SubjectIcons,
                    "subject_icons",
                    width=300,
                    height=200,
                    runs_count=3,
                    spacing=8
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            height=350,
            width=400
        )

    def _send_form_data_back(
        self,
        click_action: Callable[[list[str]], None],
        initial_subject: str
    ) -> None:

        subject_type_toggle_selected = (
            self.content.controls[2].selected[0] # type: ignore
        )
        new_subject_name = self.content.controls[0].value # type: ignore
        subject_name = initial_subject if initial_subject else new_subject_name
        subject_type = subject_type_toggle_selected
        subject_image = (self.content.controls[3] # type: ignore
        .get_selected_image_filename()
        )
        click_action([
            initial_subject,
            subject_name,
            subject_type,
            subject_image
            ]
        )

    def _reset_field(self, e: ft.ControlEvent) -> None:
        e.control.value = None # type: ignore

    def get_subject_field(self, initial_subject: str) -> ft.TextField:
        return ft.TextField(
            text_align=ft.TextAlign.CENTER,
            text_style=ft.TextStyle(
                color=ft.Colors.GREY_200,
                size=13,
            ),
            focused_bgcolor=ft.Colors.TRANSPARENT,
            label_style=ft.TextStyle(
                color=ft.Colors.GREY_200,
                size=11
            ),
            cursor_color=ft.Colors.GREY_200,
            border_color=ft.Colors.GREY_200,
            label="Subject Name",
            value=initial_subject,
            capitalization=ft.TextCapitalization.WORDS,
            max_length=35,
            input_filter= ft.InputFilter(
                allow=True,
                regex_string=r"^[a-zA-Z0-9 ]*$",
                replacement_string=""
            ),
            on_focus=self._reset_field # type: ignore
        )

    def get_subject_type_text(self) -> ft.Column:
        return ft.Column(
            controls=[
                ft.Text(
                    "Subject Type",
                    size=11,
                    weight=ft.FontWeight.W_600
                ),
                ft.Text(
                    "this is for the feed page and discord",
                    size=9,
                    weight=ft.FontWeight.W_300
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=1
        )

    def get_subject_type_toggles(self) -> ft.SegmentedButton:
        return ft.SegmentedButton(
            style=ft.ButtonStyle(
                color={
                    ft.ControlState.SELECTED: ft.Colors.BLACK,
                    ft.ControlState.DEFAULT: ft.Colors.GREY_200
                },
                bgcolor={
                    ft.ControlState.SELECTED: ft.Colors.GREEN_200
                }
            ),
            selected=["1"],
            show_selected_icon=False,
            segments=[
                ft.Segment(
                    value="1",
                    label=ft.Text("Studying", size=10)
                ),
                ft.Segment(
                    value="2",
                    label=ft.Text("Coding", size=10)
                ),
                ft.Segment(
                    value="3",
                    label=ft.Text("Practicing", size=10)
                ),
                ft.Segment(
                    value="4",
                    label=ft.Text("Working on", size=10)
                )
            ]
        )


