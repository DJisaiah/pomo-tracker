from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import flet as ft

if TYPE_CHECKING:
    from core.PomoUtils import PomoUtils
    from core.SubjectUtils import SubjectActions
    from core.Timer import Timer


class TimerModePanel(ft.Row):
    def __init__(
        self,
        utils: PomoUtils,
        timer: Timer,
        reset_timer_buttons: Callable[[bool], None],
        subject_actions: SubjectActions,
    ):
        """allows users to switch between a productive timer or a break timer

        upon toggling between either states, also resets relevant timer controls and
        actual timer states

        Args:
            utils: shared PomoUtils instance for page updates
            timer: shared Timer instance to manipulate timer states
            db: shared DBManager instance to add/edit/remove subjects
            reset_timer_buttons: callback to reset necessary controls between
                timer modes
            subject_actions: data class instance with callbacks for subject actions
        """
        super().__init__(alignment=ft.MainAxisAlignment.CENTER)
        self._utilities = utils
        self._timer = timer
        self._reset_timer_buttons = reset_timer_buttons
        self._subject_actions = subject_actions

        # UI components
        self._productive_chip = ft.Chip(
            label=ft.Text("Productive", color=ft.Colors.BLACK),
            on_select=self._productive_toggle,  # type: ignore
            selected_color=ft.Colors.GREEN_200,
            bgcolor=ft.Colors.BLACK,
            selected=True,
            show_checkmark=False,
            tooltip="Back to the grind",
        )

        self._break_chip = ft.Chip(
            label=ft.Text("Break", color=ft.Colors.WHITE),
            selected_color=ft.Colors.GREEN_200,
            bgcolor=ft.Colors.BLACK,
            enable_animation_style=ft.AnimationStyle.no_animation(),
            on_select=self._break_toggle,  # type: ignore
            show_checkmark=False,
            tooltip="Rest for a moment",
        )

        self._subject_dropdown = ft.Dropdown(
            editable=False,
            # expand=True,
            label=ft.Text(
                "Select a Subject!",
                color=ft.Colors.WHITE_70,
                size=11,
                text_align=ft.TextAlign.CENTER,
            ),
            width=150,
            color=ft.Colors.WHITE_70,
            bgcolor=ft.Colors.BLACK,
            on_select=self._update_current_subject,  # type: ignore
        )
        self._subject_dropdown.options = self._get_subjects()  # type: ignore

        self._add_subject_button = ft.IconButton(
            icon=ft.Icons.ADD,
            icon_size=19,
            icon_color=ft.Colors.GREY_400,
            tooltip="Add a new subject",
            on_click=self._add_subject,  # type: ignore
        )

        self.controls = [
            ft.Row(
                controls=[
                    self._productive_chip,
                    self._break_chip,
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
            ft.Row(controls=[self._subject_dropdown, self._add_subject_button]),
        ]

    def _productive_toggle(self, e: ft.ControlEvent | None = None) -> None:
        # update colours
        self._productive_chip.selected = True
        self._productive_chip.label.color = ft.Colors.BLACK  # type: ignore

        self._break_chip.selected = False
        self._break_chip.label.color = ft.Colors.WHITE  # type: ignore

        # switch to productive timer
        self._timer.productive_mode()
        self._reset_timer_buttons(True)

        self._utilities.update_page()

    def _break_toggle(self, e: ft.ControlEvent) -> None:
        # update colours
        self._break_chip.selected = True
        self._break_chip.label.color = ft.Colors.BLACK  # type: ignore

        self._productive_chip.selected = False
        self._productive_chip.label.color = ft.Colors.WHITE  # type: ignore

        # switch to break timer
        self._timer.break_mode()
        self._reset_timer_buttons(False)

        self._utilities.update_page()

    def _update_menu(self) -> None:
        self._subject_dropdown.options = self._get_subjects()  # type: ignore
        self._utilities.update_page()

    def _update_current_subject(self, e: ft.ControlEvent):
        subject_name: str = e.control.data
        if subject_name is None:
            subject_name: str = e.control.value
        self._subject_actions.update_subject(subject_name)  # type: ignore

    def _add_subject(self, e: ft.ControlEvent) -> None:
        self._subject_actions.add(self._update_menu)

    def _remove_subject(self, e: ft.ControlEvent) -> None:
        subject_name: str = e.control.data
        self._subject_actions.remove(subject_name)
        self._subject_dropdown.value = ""
        if self._subject_actions.current_subject == subject_name:
            self._subject_actions.update_subject(None)
        self._update_menu()

    def _edit_subject(
        self,
        e: ft.ControlEvent,
    ) -> None:
        subject_name: str = e.control.data
        self._subject_actions.edit(subject_name, self._update_menu)

    def _get_subjects(self) -> list[str]:
        subjects_options = []
        all_subjects: list[tuple[int, str]] = self._subject_actions.get_all()

        max_name_size = 0
        for subject_id, subject in all_subjects:
            max_name_size = max(len(subject), max_name_size)
            subjects_options.append(
                ft.DropdownOption(
                    text=subject,
                    content=ft.Row(
                        controls=[
                            ft.Text(f"{subject}", color=ft.Colors.WHITE_70, size=11),
                            ft.Row(
                                controls=[  # type: ignore
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        icon_size=20,
                                        on_click=self._edit_subject,  # type: ignore
                                        data=subject,
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_FOREVER,
                                        icon_size=20,
                                        on_click=self._remove_subject,  # type: ignore
                                        data=subject,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                spacing=-8,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                )
            )

        self._subject_dropdown.menu_width = 12 * max_name_size + 60
        if len(all_subjects) >= 7:
            self._subject_dropdown.menu_height = 300

        return subjects_options
