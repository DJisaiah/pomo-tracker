from __future__ import annotations
from typing import Callable, List, Dict, TYPE_CHECKING
import flet as ft
from core.enums import SubjectIcons, SubjectType
from core.SubjectUtilities import SubjectUtilities


if TYPE_CHECKING:
    from core.PomoUtilities import PomoUtilities
    from database.LocalDB import LocalDB
    from pages.TimerPage import TimerPage.TimerPageUtilities
    from core.Timer import Timer


class TimerModeAndSubjectControls:
    def __init__(self, utilities):
        self._tp_utilities: TimerPageUtilities = utilities
        self._utilities: PomoUtilities = self._tp_utilities.get_utilities()
        self._timer: Timer = self._tp_utilities.get_timer()
        self._db: LocalDB = self._tp_utilities.get_utilities().get_db()
        self._set_timer_text: Callable[[str], [None]] = self._tp_utilities.set_timer_text
        self._update_current_subject: Callable[[str], [None]] = self._tp_utilities.update_current_subject
        self._get_current_subject: Callabe[[None], [None]] = self._tp_utilities.get_current_subject
        

        # controls
        self._productive_chip = ft.Chip(
                label=ft.Text("Productive", color=ft.Colors.BLACK),
                on_select=self._productive_toggle,
                selected_color=ft.Colors.GREEN_200,
                bgcolor=ft.Colors.BLACK,
                selected=True,
                show_checkmark=False,
                tooltip="Back to the grind"
            )
        
        self._break_chip = ft.Chip(
                label=ft.Text("Break", color=ft.Colors.WHITE),
                selected_color=ft.Colors.GREEN_200,
                bgcolor=ft.Colors.BLACK,
                enable_animation_style=ft.AnimationStyle.no_animation(),
                on_select=self._break_toggle,
                show_checkmark=False,
                tooltip="Rest for a moment"
            )

        self._subject_dropdown = ft.Dropdown(
                editable=False,
                #expand=True,
                label=ft.Text("Select a Subject!",
                    color=ft.Colors.WHITE_70,
                    size=11,
                    text_align=ft.TextAlign.CENTER
                ),
                width=150,
                
                color=ft.Colors.WHITE_70,
                bgcolor=ft.Colors.BLACK,
                on_select=self._update_current_subject
            )
        self._subject_dropdown.options=self._get_subjects()
        self._subject_utilities = SubjectUtilities(
            self._utilities, 
            self._subject_dropdown.options, 
            self._db,
            self._update_menu
        )

        self._add_subject_button = ft.IconButton(
                icon=ft.Icons.ADD,
                icon_size=19,
                icon_color=ft.Colors.GREY_400,
                tooltip="Add a new subject",
                on_click=self._add_subject,
            )


        self._timer_mode_and_subject_controls = ft.Row(
            controls=[
                ft.Row(controls=[
                    self._productive_chip,
                    self._break_chip,               
                ], alignment=ft.MainAxisAlignment.END),
                ft.Row(controls=[
                    self._subject_dropdown,
                    self._add_subject_button           
                ])
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                #spacing=5
        )

    def get_components(self) -> ft.Row:
        return self._timer_mode_and_subject_controls

    def _productive_toggle(self, e: ft.ControlEvent=None) -> None:
        # update colours
        self._productive_chip.selected = True
        self._productive_chip.label.color = ft.Colors.BLACK

        self._break_chip.selected = False
        self._break_chip.label.color = ft.Colors.WHITE


        # switch to productive timer
        self._timer.productive_mode()
        new_time = f"{self._timer.get_pomo_length()}:00"
        self._set_timer_text(new_time)
        self._tp_utilities.reset_start_stop()

        self._utilities.update_page()

    def _break_toggle(self, e: ft.ControlEvent) -> None:
        # update colours
        self._break_chip.selected = True
        self._break_chip.label.color = ft.Colors.BLACK

        self._productive_chip.selected = False
        self._productive_chip.label.color = ft.Colors.WHITE

        # switch to break timer
        self._timer.break_mode()
        new_time = f"{self._timer.get_break_length():02d}:00"
        self._set_timer_text(new_time)
        self._tp_utilities.reset_start_stop()

        self._utilities.update_page()
    
    def _update_menu(self) -> None:
        self._subject_dropdown.options = self._get_subjects()
        self._utilities.update_page()

    def _if_dropdown_empty(self) -> None:
        if not self._subject_dropdown.options:
            self._subject_dropdown.menu_height = 0
            return True
        else: 
            self._subject_dropdown.menu_height = 300
            return False

    
    def _add_subject(self, e: ft.ControlEvent) -> None:
        self._subject_utilities.add_subject()

    def _remove_subject(self, e: ft.ControlEvent) -> None:
        subject_name = e.control.parent.parent.controls[0].value
        self._subject_dropdown.value = ""
        if self._get_current_subject() == subject_name:
            self._update_current_subject(None)
        self._db.remove_subject(subject_name)

    def _edit_subject(self, e: ft.ControlEvent, subject_name_given: str=None) -> None:
        if subject_name_given:
            subject_name = subject_name_given
        elif e is None:
            subject_name = ""
        else:
            subject_name = e.control.parent.parent.controls[0].value
        self._subject_utilities.edit_subject(subject_name)

    def _get_subjects(self) -> List[str]:
        subjects_options = []
        all_subjects: Dict[str, str] = self._db.get_all_subjects()

        max_name_size = 0
        print(all_subjects)
        for subject_id, subject in all_subjects:
            max_name_size = max(len(subject), max_name_size)
            subjects_options.append(
                ft.DropdownOption(
                    text=subject,
                    content=ft.Row(
                        controls=[
                            ft.Text(
                                f"{subject}", 
                                color=ft.Colors.WHITE_70,
                                size=11
                            ),
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        icon_size=20,
                                        on_click=self._edit_subject
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_FOREVER,
                                        icon_size=20,
                                        on_click=self._remove_subject
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                spacing=-8
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                )
            )

        self._subject_dropdown.menu_width = 12 * max_name_size + 60
        if len(all_subjects) >= 7:
            self._subject_dropdown.menu_height=300

        return subjects_options

