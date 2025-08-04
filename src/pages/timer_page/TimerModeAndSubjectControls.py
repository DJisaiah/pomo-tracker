import flet as ft

class TimerModeAndSubjectControls:
    def __init__(self, page, timer, database):
        self._page = page
        self._timer = timer
        self._db = database

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
                label="Select a Subject!",
                options=self._get_subjects(),
                width=150
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
        self._productive_chip.selected = False
        self._productive_chip.label.color = ft.Colors.WHITE
        e.control.label.color = ft.Colors.BLACK

        # switch to productive timer
        self._set_timer_text("25:00")
        self._timer.productive_mode()

        self._page.update()

    def _break_toggle(self, e):
        # update colours
        self._break_chip.selected = False
        self._break_chip.label.color = ft.Colors.WHITE
        e.control.label.color = ft.Colors.BLACK

        # switch to break timer
        self._set_timer_text("05:00")
        self._timer.break_mode()

        self._page.update()
    
    def _update_menu(self):
        self._subject_dropdown.options = self._get_subjects()
        self._page.update()

    
    def _add_subject(self, e):

        def send_subject_to_db(e):
            text_field = dlg_content.controls[0]
            user_subject = text_field.value

            if user_subject == "":
                return

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
                    input_filter=ft.InputFilter(regex_string=r"[a-zA-Z0-9 ]") # input filter bug in flet so will have to do this manually
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

        dlg = ft.AlertDialog(
            title=ft.Text("Enter a Subject"),
            content=dlg_content,
            alignment=ft.alignment.center,
            on_dismiss=lambda e: print("dialog dismissed"),
            surface_tint_color=ft.Colors.BLACK
        )
        self._page.open(dlg)

    def _remove_subject(self, e):
        self._db.remove_subject(e.control.parent.parent.key)
        self._update_menu()

    def _get_subjects(self):
        subjects_options = []
        all_subjects = self._db.get_all_subjects()

        for subject_id, subject in all_subjects:
            subjects_options.append(
                ft.DropdownOption(
                    key=[subject_id],
                    content=ft.Row(
                        controls=[
                            ft.Text(f"{subject}"),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_FOREVER,
                                on_click=self._remove_subject
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                )
            )

        return subjects_options


