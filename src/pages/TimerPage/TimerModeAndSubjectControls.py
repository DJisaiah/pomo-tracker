from __future__ import annotations
from typing import Callable, List, Dict, TYPE_CHECKING
import flet as ft


if TYPE_CHECKING:
    from core.PomoUtilities import PomoUtilities

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
                menu_width=400,
                options=self._get_subjects(),
                #menu_height=300,
                color=ft.Colors.WHITE_70,
                bgcolor=ft.Colors.BLACK,
                #on_focus=self._if_dropdown_empty,
                #on_select=self._update_current_subject
            )
        #self._subject_dropdown.options=self._get_subjects(),

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
        def valid_subject(subject_name: str) -> bool:
            # check subject is not a duplicate
            subjects = self._subject_dropdown.options
            if subject_name.strip(" ") == "":
                self._utilities.alert_user("Invalid Subject", "Subject name can't be empty.")
                return False
            for subject in subjects:
                subject_text = subject.text
                if subject_text == subject_name:
                    self._utilities.alert_user("Invalid Subject", "Subject already exists.")
                    return False
            return True

        def send_subject_to_db(e: ft.ControlEvent=None) -> None:

            text_field = dlg_content.controls[0]
            user_subject = text_field.value

            if not valid_subject(user_subject):
                return
            self._utilities.close_dialog()
            self._utilities.text_toast("Subject added")

            self._db.add_subject(user_subject)
            self._update_menu()
        
        dlg_content = ft.Row(
            controls=[
                ft.TextField(
                    color=ft.Colors.GREEN_300,
                    border_color=ft.Colors.GREEN_300,
                    label=ft.Text("Your Subject Name",color=ft.Colors.WHITE_70),
                    #selection_color=ft.Colors.GREY_500,
                    capitalization=ft.TextCapitalization.WORDS,
                    max_length=40,
                    input_filter= ft.InputFilter(
                        allow=True,
                        regex_string=r"^[a-zA-Z0-9 ]*$",
                        replacement_string=""
                        )
                    )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        self._utilities.generic_alert("Enter a Subject", dlg_content, send_subject_to_db)

    def _remove_subject(self, e: ft.ControlEvent) -> None:
        subject_name = e.control.parent.parent.controls[0].value
        self._subject_dropdown.value = ""
        if self._get_current_subject() == subject_name:
            self._update_current_subject(None)
        self._db.remove_subject(subject_name)
        self._update_menu()

    def _edit_subject(self, e: ft.ControlEvent) -> None:
        pass

    def _get_subjects(self) -> List[str]:
        subjects_options = []
        all_subjects: Dict[str, str] = self._db.get_all_subjects()

        for subject_id, subject in all_subjects:
            subjects_options.append(
                ft.DropdownOption(
                    text=subject,
                    content=ft.Row(
                        controls=[
                            ft.Text(f"{subject}", color=ft.Colors.WHITE_70),
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

        #if not subjects_options:
        #    self._subject_dropdown.height = 10
        #    return None
        #else:
        #    self._subject_dropdown.height = 300

        return subjects_options

