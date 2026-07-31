from typing import Callable

import flet as ft

from components.base.ImagePicker import ImagePicker
from core.enums import StyleTokens, SubjectIcons, SubjectType


class SubjectEditor(ft.AlertDialog):
    def __init__(
        self, click_action: Callable[[list[str]], None], initial_subject: str = ""
    ):
        """prompt the user for a subject name, subject type, subject image
        performs a callback action based on that data

        upon submission the data is passed as a list (in the order prompted)
        as parameters to the callback with the intial subject (first)

        Args:
            click_action: callback function that accepts a list of strings as params
            initial_subject: str subject name to prepopulate form
        """
        super().__init__(
            bgcolor=StyleTokens.CONTAINER_GREY.value,
            alignment=ft.Alignment.CENTER,
            content_padding=ft.Padding(bottom=30, top=30),
            shape=ft.RoundedRectangleBorder(
                radius=10, side=ft.BorderSide(color=ft.Colors.GREY_900, width=1)
            ),
        )

        self.actions = [
            ft.TextButton(
                content=ft.Text(
                    "Cool.", color=ft.Colors.BLACK, font_family="Inter-Bold"
                ),
                on_click=lambda e: self._send_form_data_back(
                    click_action, initial_subject
                ),
                style=ft.ButtonStyle(
                    bgcolor=StyleTokens.POMO_GREEN.value,
                    overlay_color=ft.Colors.GREEN_300,
                ),
            )
        ]

        self._subject_field = self.get_subject_field(initial_subject)
        self._subject_type_toggles = self.get_subject_type_toggles()
        self._image_picker = ImagePicker(
            SubjectIcons,
            "subject_icons",
            width=300,
            height=200,
            runs_count=3,
            spacing=8,
            tooltip=ft.Tooltip(
                message="Subject image to show in feed and to friends",
                bgcolor=StyleTokens.CONTAINER_LIGHTER_GREY.value,
                text_style=ft.TextStyle(color=ft.Colors.WHITE),
                vertical_offset=100,
            ),
        )
        self._form_error_text = self.get_form_error_text()

        self.content = ft.Column(
            controls=[
                self._subject_field,
                self._subject_type_toggles,
                self._image_picker,
                self._form_error_text,
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            height=350,
            width=400,
            expand=True,
        )

    def _send_form_data_back(
        self, click_action: Callable[[list[str]], None], initial_subject: str
    ) -> None:
        name_field = self._subject_field
        new_subject_name = (name_field.value or "").strip()
        if not new_subject_name:
            self.form_error_text.value = "Subject name cannot be empty."
            self.form_error_text.visible = True
            self.form_error_text.update()
            return
        self.form_error_text.visible = False
        self.form_error_text.update()
        subject_type_selected = self._subject_type_toggles.selected[0]
        subject_type: str = SubjectType.from_id(subject_type_selected)
        selected_image = self._image_picker.get_selected_image_filename()
        if selected_image is None:
            self.form_error_text.value = "You have to select an icon!"
            self.form_error_text.visible = True
            self.form_error_text.update()
            return
        subject_image = SubjectIcons(selected_image).name
        click_action([initial_subject, new_subject_name, subject_type, subject_image])

    def _reset_field(self, e: ft.Event[ft.TextField]) -> None:
        e.control.value = ""
        e.control.label = None

    def _on_blur(self, e: ft.Event[ft.TextField]) -> None:
        e.control.label = "Subject Name"

    def get_form_error_text(self) -> ft.Text:
        form_error_text = ft.Text(
            color=ft.Colors.RED_400,
            size=14,
            visible=False,
        )
        self.form_error_text = form_error_text
        return form_error_text

    def get_subject_field(self, initial_subject: str) -> ft.TextField:
        return ft.TextField(
            text_align=ft.TextAlign.CENTER,
            text_style=ft.TextStyle(
                color=ft.Colors.GREY_200,
                size=13,
            ),
            bgcolor=StyleTokens.CONTAINER_LIGHTER_GREY.value,
            border_radius=10,
            focused_border_color=StyleTokens.POMO_GREEN.value,
            label_style=ft.TextStyle(color=ft.Colors.GREY_200, size=11),
            label="Subject Name",
            value=initial_subject,
            capitalization=ft.TextCapitalization.WORDS,
            max_length=35,
            input_filter=ft.InputFilter(
                allow=True, regex_string=r"^[a-zA-Z0-9 ]*$", replacement_string=""
            ),
            on_focus=self._reset_field,
            on_blur=self._on_blur,
        )

    def get_subject_type_toggles(self) -> ft.SegmentedButton:
        return ft.SegmentedButton(
            width=300,
            style=ft.ButtonStyle(
                color={
                    ft.ControlState.SELECTED: ft.Colors.BLACK,
                    ft.ControlState.DEFAULT: ft.Colors.GREY_200,
                },
                bgcolor={ft.ControlState.SELECTED: StyleTokens.POMO_GREEN.value},
            ),
            selected=["1"],
            show_selected_icon=False,
            segments=[
                ft.Segment(
                    value=str(v),
                    label=ft.Text(
                        s,
                        size=9,
                        font_family="Inter-Bold",
                    ),
                )
                for v, s in enumerate(
                    ["Studying", "Coding", "Practicing", "Working on"], start=1
                )
            ],
            tooltip=ft.Tooltip(
                message="Subject type to show on discord and in feed",
                bgcolor=StyleTokens.CONTAINER_LIGHTER_GREY.value,
                text_style=ft.TextStyle(color=ft.Colors.WHITE),
                prefer_below=True,
            ),
        )
