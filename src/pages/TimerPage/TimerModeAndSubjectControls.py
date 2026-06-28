from __future__ import annotations
from typing import Callable, List, Dict, TYPE_CHECKING
import flet as ft
from core.enums import SubjectIcons


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
                
                color=ft.Colors.WHITE_70,
                bgcolor=ft.Colors.BLACK,
                on_select=self._update_current_subject
            )
        self._subject_dropdown.options=self._get_subjects()

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
                    max_length=35,
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

    def _edit_subject(self, e: ft.ControlEvent=None) -> None:
        dlg = self._utilities._get_generic_dialog() 
        dlg.content_padding = ft.Padding(bottom=50)
        if e is None:
            subject_name = ""
        else:
            subject_name = e.control.parent.parent.controls[0].value

        def reset_field(e: ft.ControlEvent) -> None:
            e.control.value = None

        subject_field = ft.TextField(
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
            value=subject_name,
            capitalization=ft.TextCapitalization.WORDS,
            max_length=35,
            input_filter= ft.InputFilter(
                allow=True,
                regex_string=r"^[a-zA-Z0-9 ]*$",
                replacement_string=""
            ),
            on_focus=reset_field
        )

        subject_type_text = ft.Column(
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

        subject_type_toggles = ft.SegmentedButton(
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

        def get_images() -> list[ft.Image]:

            def image_on_hover(e: ft.ControlEvent) -> None:
                e.control.border = ft.Border.all(
                    width=3,
                    color=ft.Colors.GREEN_200
                ) if e.data else None

            def image_dehover(e: ft.ControlEvent) -> None:
                e.control.border = None

            images = []
            for filename in SubjectIcons:
                image = ft.Image(
                    src=f"subject_icons/{filename}",
                )

                image_container = ft.Container(
                    content=image,
                    on_hover=image_on_hover,
                    bgcolor=ft.Colors.WHITE_10
                )
                
                
                images.append(image_container)
            return images
                
    
        subject_image_picker = ft.Column(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            "Subject Image",
                            size=11,
                            weight=ft.FontWeight.W_600
                        ),
                        ft.Text(
                            "this is for the feed page",
                            size=9,
                            weight=ft.FontWeight.W_300
                        )
                    ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=1
                ),
                ft.GridView(
                    width=300,
                    height=200,
                    runs_count=3,
                    spacing=8,
                    controls=get_images(),
                    scroll=ft.ScrollMode.ALWAYS, 
                )
            ],
            height=300,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2
        )

        dlg.content = ft.Column(
            controls=[
                subject_field,
                subject_type_text,
                subject_type_toggles,
                subject_image_picker
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            height=350,
            width=400
        )

        self._utilities.show_dialog(dlg)

    def _get_subjects(self) -> List[str]:
        subjects_options = []
        all_subjects: Dict[str, str] = self._db.get_all_subjects()

        max_name_size = 0
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

