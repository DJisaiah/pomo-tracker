import flet as ft
from core.PomoUtilities import PomoUtilities as utilities

class TimerModeAndSubjectControls:
    def __init__(self, utilities, timer, database, set_timer_text, update_current_subject, get_current_subject):
        self._utilities = utilities
        self._timer = timer
        self._db = database
        self._set_timer_text = set_timer_text
        self._update_current_subject = update_current_subject
        self._get_current_subject = get_current_subject


        self._productive_chip = ft.Chip(
                label=ft.Text("Productive", color=ft.Colors.BLACK),
                on_select=self._productive_toggle,
                selected_color=ft.Colors.GREEN_200,
                selected=True,
                show_checkmark=False,
                tooltip="Back to the grind"
            )
        
        self._break_chip = ft.Chip(
                label=ft.Text("Break", color=ft.Colors.WHITE),
                selected_color=ft.Colors.GREEN_200,
                on_select=self._break_toggle,
                show_checkmark=False,
                tooltip="Rest for a moment"
            )

        self._subject_dropdown = ft.Dropdown(
                editable=False,
                expand=True,
                label="Select a Subject!",
                options=self._get_subjects(),
                width=150,
                menu_width=250,
                on_change=self._update_current_subject
            )

        self._add_subject_button = ft.IconButton(
                icon=ft.Icons.ADD,
                icon_size=19,
                icon_color=ft.Colors.GREY_400,
                tooltip="Add a new subject",
                on_click=self._add_subject,
            )


        self._timer_mode_and_subject_controls = ft.Row(controls=[
            self._productive_chip,
            self._break_chip,
            self._subject_dropdown,
            self._add_subject_button
            ], 
            alignment=ft.MainAxisAlignment.CENTER
        )

    def get_components(self):
        return self._timer_mode_and_subject_controls

    def _productive_toggle(self, e):
        # update colours
        self._productive_chip.selected = True
        self._productive_chip.label.color = ft.Colors.WHITE
        e.control.label.color = ft.Colors.BLACK

        self._break_chip.selected = False
        self._break_chip.label.color = ft.Colors.WHITE


        # switch to productive timer
        self._set_timer_text("25:00")
        self._timer.productive_mode()

        self._utilities.update_page()

    def _break_toggle(self, e):
        # update colours
        self._break_chip.selected = True
        self._break_chip.label.color = ft.Colors.WHITE
        e.control.label.color = ft.Colors.BLACK

        self._productive_chip.selected = False
        self._productive_chip.label.color = ft.Colors.WHITE

        # switch to break timer
        self._set_timer_text("05:00")
        self._timer.break_mode()

        # update rpc
        self._utilities.get_RPC().update_details("On break")

        self._utilities.update_page()
    
    def _update_menu(self):
        self._subject_dropdown.options = self._get_subjects()
        self._utilities.update_page()

    
    def _add_subject(self, e):
        def valid_subject(subject_name):
            # check subject is not a duplicate
            subjects = self._subject_dropdown.options
            for subject in subjects:
                subject_text = subject.text
                if subject_name.strip(" ") == "":
                    utilities.warn_user("Invalid Subject. Subject name can't be empty")
                if subject_text == subject_name:
                    utilities.warn_user("Invalid Subject. Subject already exists.")
                    return False
            return True

        def send_subject_to_db(e):

            text_field = dlg_content.controls[0]
            user_subject = text_field.value

            if user_subject == "":
                return
            elif not valid_subject(user_subject):
                return
            #dlg.open = False
            self._utilities.close_dialog()
            self._utilities.text_toast("Subject added")

            self._db.add_subject(user_subject)
            self._update_menu()
        
        dlg_content = ft.Row(
            controls=[
                ft.TextField(
                    width=200,
                    color=ft.Colors.GREEN_300,
                    border_color=ft.Colors.GREEN_300,
                    label="Your subject name",
                    selection_color=ft.Colors.GREY_500,
                    capitalization=ft.TextCapitalization.WORDS,
                    max_length=20
                    #input_filter=ft.InputFilter(allow=False, regex_string=r"[^!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?`~]+"),  input filter bug in flet so will have to do this manually
                ),
                ft.IconButton(
                    icon=ft.Icons.SAVE,
                    icon_color=ft.Colors.GREEN_300,
                    on_click=send_subject_to_db
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        # dlg = ft.AlertDialog(
        #     title=ft.Text("Enter a Subject"),
        #     content=dlg_content,
        #     alignment=ft.alignment.center,
        #     surface_tint_color=ft.Colors.BLACK
        # )
        #self._page.open(dlg)
        self._utilities.generic_alert("Enter a Subject", dlg_content)

    def _remove_subject(self, e):
        subject_name = e.control.parent.controls[0].value
        subject_id = e.control.content.value
        self._subject_dropdown.value = ""
        if self._get_current_subject() == subject_name:
            self._update_current_subject(None)
        self._db.remove_subject(subject_id)
        self._update_menu()

    def _get_subjects(self):
        subjects_options = []
        all_subjects = self._db.get_all_subjects()

        for subject_id, subject in all_subjects:
            subjects_options.append(
                ft.DropdownOption(
                    text=subject,
                    content=ft.Row(
                        controls=[
                            ft.Text(f"{subject}"),
                            ft.IconButton(
                                content=ft.Text(f"{subject_id}"),
                                icon=ft.Icons.DELETE_FOREVER,
                                on_click=self._remove_subject
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                )
            )

        return subjects_options

