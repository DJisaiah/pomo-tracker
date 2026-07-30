from typing import TYPE_CHECKING

import flet as ft

from core.enums import StyleTokens

if TYPE_CHECKING:
    from core.PomoUtils import PomoUtils
    from core.SubjectUtils import SubjectActions


class SubjectPicker(ft.Row):
    def __init__(self, subject_actions: SubjectActions, utilities: PomoUtils):
        self._subject_actions = subject_actions
        self._utilities = utilities
        super().__init__(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self._text_label = ft.Text(
            "____",
            color=StyleTokens.POMO_GREEN.value,
            weight=ft.FontWeight.W_500,
            font_family="Space Grotesk",
            size=20,
        )
        self._subject_picker = ft.PopupMenuButton(
            icon=ft.Row(
                controls=[self._text_label, ft.Icon(icon=ft.Icons.EXPAND_MORE)]
            ),
            menu_position=ft.PopupMenuPosition.UNDER,
            bgcolor=StyleTokens.POMO_MENU.value,
            shape=ft.RoundedRectangleBorder(radius=10),
            size_constraints=ft.BoxConstraints(
                max_height=300,
                max_width=600,
            ),
        )

        self._subject_picker.items = self._get_subjects()
        self.controls = [
            ft.Text(
                "Today,",
                color=StyleTokens.POMO_GREEN.value,
                weight=ft.FontWeight.W_500,
                font_family="Space Grotesk",
                size=20,
            ),
            ft.Text(
                "I want to study",
                weight=ft.FontWeight.W_400,
                font_family="Space Grotesk",
            ),
            self._subject_picker,
        ]

    def update_menu(self) -> None:
        self._subject_picker.items = self._get_subjects()
        self._subject_picker.update()

    def _update_current_subject(self, e: ft.Event[ft.PopupMenuItem]):
        subject_name: str = e.control.data
        if subject_name is None:
            return
            subject_name: str = e.control.data
        self._subject_actions.update_subject(subject_name)  # type: ignore
        if len(subject_name) >= 10:
            subject_name = f"{subject_name[0:7]}..."
        self._text_label.value = subject_name
        self._text_label.update()

    def _add_subject(self, e: ft.Event[ft.Button]) -> None:
        self._subject_actions.add(self.update_menu)

    def _remove_subject(self, e: ft.ControlEvent) -> None:
        subject_name: str = e.control.data
        self._show_delete_confirmation(subject_name)
        self._text_label.value = "____"

    def _show_delete_confirmation(self, subject_name: str) -> None:
        def confirm_delete(e: ft.ControlEvent) -> None:
            self._subject_actions.remove(subject_name)
            self._text_label.value = "____"
            if self._subject_actions.current_subject == subject_name:
                self._subject_actions.update_subject(None)
            self.update_menu()
            self._utilities.close_dialog()

        def cancel_delete(e: ft.ControlEvent) -> None:
            self._utilities.close_dialog()

        dialog = ft.AlertDialog(
            bgcolor=ft.Colors.BLACK,
            title=ft.Text(
                f"Delete {subject_name}?",
                text_align=ft.TextAlign.CENTER,
                color=ft.Colors.WHITE_70,
            ),
            content=ft.Text(
                "This action cannot be undone.",
                text_align=ft.TextAlign.CENTER,
                color=ft.Colors.WHITE_70,
                size=12,
            ),
            alignment=ft.Alignment.CENTER,
            shape=ft.RoundedRectangleBorder(
                radius=10, side=ft.BorderSide(color=ft.Colors.GREY_700, width=2)
            ),
            actions=[  # type: ignore
                ft.TextButton(
                    content=ft.Text("Cancel", color=ft.Colors.GREY_400),
                    on_click=cancel_delete,  # type: ignore
                ),
                ft.TextButton(
                    content=ft.Text(
                        "Confirm", color=ft.Colors.RED_400, weight=ft.FontWeight.BOLD
                    ),
                    on_click=confirm_delete,  # type: ignore
                ),
            ],
        )
        self._utilities.show_dialog(dialog)

    def _edit_subject(
        self,
        e: ft.ControlEvent,
    ) -> None:
        subject_name: str = e.control.data
        self._subject_actions.edit(subject_name, self.update_menu)

    def _get_subjects(self) -> list[ft.PopupMenuItem]:
        subjects_options = [
            ft.PopupMenuItem(
                content=ft.Column(
                    controls=[
                        ft.Button(
                            icon=ft.Icons.ADD,
                            icon_color=ft.Colors.WHITE,
                            bgcolor="#6EA8FE",
                            content=ft.Text(
                                "Add Subject",
                                color=ft.Colors.WHITE,
                                weight=ft.FontWeight.W_700,
                            ),
                            on_click=self._add_subject,
                        ),
                        ft.Divider(color=ft.Colors.GREY_700, thickness=1),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            )
        ]
        all_subjects: list[tuple[int, str]] = self._subject_actions.get_all()

        max_name_size = 0
        for subject_id, subject in all_subjects:
            max_name_size = max(len(subject), max_name_size)
            subjects_options.append(
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[
                            ft.Text(
                                f"{subject}",
                                color=ft.Colors.WHITE,
                                weight=ft.FontWeight.W_600,
                            ),
                            ft.Row(
                                controls=[  # type: ignore
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        icon_size=20,
                                        on_click=self._edit_subject,  # type: ignore
                                        data=subject,
                                        icon_color=ft.Colors.GREY_200,
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_FOREVER,
                                        icon_size=20,
                                        on_click=self._remove_subject,  # type: ignore
                                        data=subject,
                                        icon_color=ft.Colors.RED,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                spacing=-8,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    on_click=self._update_current_subject,
                    data=subject,
                )
            )
        return subjects_options
