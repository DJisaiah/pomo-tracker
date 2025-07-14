import flet as ft
from core.timer import Timer
from database.local_db import LocalDB

class TimerPage:
    def __init__(self, page: ft.Page):
        self._page = page
        self._POMODORO = 25
        self._BREAK = 5
        self._buttons_toggled = False
        self._CURRENT_SUBJECT = None
        self._db = LocalDB()

        self._timer = Timer(self._POMODORO, self._BREAK, self)


        def productive_toggle(e):
            # update colours
            self._study_break_subject_bar.controls[1].selected = False
            self._study_break_subject_bar.controls[1].label.color = ft.Colors.WHITE
            e.control.label.color = ft.Colors.BLACK

            # switch to productive timer
            self._set_timer_text("25:00")
            self._timer.productive_mode()

            self._page.update()

        def break_toggle(e):
            # update colours
            self._study_break_subject_bar.controls[0].selected = False
            self._study_break_subject_bar.controls[0].label.color = ft.Colors.WHITE
            e.control.label.color = ft.Colors.BLACK

            # switch to break timer
            self._set_timer_text("05:00")
            self._timer.break_mode()

            self._page.update()
        
        def add_subject(e):

            def send_subject_to_db(e):
                text_field = dlg_content.controls[0]
                user_subject = text_field.value

                if user_subject == "":
                    return

                self._db.add_subject(user_subject)

            dlg_content = ft.Row(
                controls=[
                    ft.TextField(
                        width=200,
                        color=ft.Colors.GREEN_300,
                        border_color=ft.Colors.GREEN_300,
                        label="Your subject name",
                        selection_color=ft.Colors.GREY_500,
                        capitalization=ft.TextCapitalization.WORDS,
                        input_filter=ft.TextOnlyInputFilter()
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

        def get_subjects():
            subjects_options = []
            all_subjects = self._db.get_all_subjects()

            for id, subject in all_subjects:
                subjects_options.append(
                    ft.DropdownOption(
                        key=[id],
                        text=ft.Text(f"{subject}")
                    )
                )

            return subjects_options


        self._study_break_subject_bar = ft.Row(controls=[
            ft.Chip(
                label=ft.Text("Productive", color=ft.Colors.BLACK),
                on_select=productive_toggle,
                selected_color=ft.Colors.GREEN_300,
                selected=True,
                show_checkmark=False,
                tooltip="Back to the grind"
            ),
            ft.Chip(
                label=ft.Text("Break", color=ft.Colors.WHITE),
                selected_color=ft.Colors.GREEN_300,
                on_select=break_toggle,
                show_checkmark=False,
                tooltip="Rest for a moment"
            ),
            ft.Dropdown(
                editable=True,
                label="Select a Subject!",
                options=get_subjects()
            ),
            ft.IconButton(
                icon=ft.Icons.ADD,
                icon_size=20,
                icon_color=ft.Colors.GREY_500,
                tooltip="Add a new subject",
                on_click=add_subject,
            )
            ], 
            alignment=ft.MainAxisAlignment.CENTER
        )

        def stopwatch_mode(e):
            self._timer.stopwatch_toggle()
            self._set_timer_text("00:00")
            self._page.update()

        self._buttons = ft.Row(controls=[
            ft.IconButton(
                icon=ft.Icons.PLAY_CIRCLE,
                icon_size=90,
                tooltip="Start the timer",
                icon_color=ft.Colors.GREEN_300,
                on_click=self._timer.start_timer,
            ),
            ft.IconButton(
                icon=ft.Icons.STOP_CIRCLE,
                icon_size=90,
                icon_color=ft.Colors.GREY_500,
                tooltip="Stop the timer",
                on_click=self._timer.stop_timer,
                disabled=True
                
            ),
            ft.Container(content=
                ft.CircleAvatar(
                    content=ft.Text("Stopwatch \n Mode", text_align=ft.TextAlign.CENTER, size=10),
                    radius=40,
                    bgcolor=ft.Colors.BLUE_GREY_900,
                    tooltip="Act as a stopwatch and stop when the user wants",
                ),
                on_click=stopwatch_mode
            ),
        ], 
        alignment=ft.MainAxisAlignment.CENTER,
        )

        def increase_timer(e):
            self._timer.increase_timer()
            self._page.update()

        def decrease_timer(e):
            self._timer.decrease_timer()
            self._page.update()

        self._timer_and_inc_dec_buttons = ft.Row(controls=[
            ft.Row(controls=[
                ft.Text("25:00", size=150),
                ft.Column(controls=[
                    ft.IconButton(
                        icon=ft.Icons.ARROW_UPWARD,
                        icon_size = 30,
                        icon_color=ft.Colors.BLUE_GREY_600,
                        tooltip="Increase timer by 5mins",
                        on_click=increase_timer
                    ),
                    ft.IconButton(
                        icon=ft.Icons.ARROW_DOWNWARD,
                        icon_size = 30,
                        icon_color=ft.Colors.BLUE_GREY_600,
                        tooltip="Decrease timer by 5mins",
                        on_click=decrease_timer
                    )
                ])
            ])
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=80
        )

        self._timer_and_controls = ft.Column(controls=[
            self._study_break_subject_bar,
            self._timer_and_inc_dec_buttons,
            self._buttons
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=0,
        )

        self._page_layout = ft.Column(controls=[
            ft.Container(),
            self._timer_and_controls
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
        )

    def get_page(self):
        return self._page_layout
    
    def _set_timer_text(self, new_text):
        text = self._timer_and_inc_dec_buttons.controls[0].controls[0]
        text.value = new_text
    
    def toggle_start_stop(self):
        play_button = self._buttons.controls[0]
        stop_button = self._buttons.controls[1]

        if self._buttons_toggled:
            play_button.disabled = False
            play_button.icon_color = ft.Colors.GREEN_300
            stop_button.disabled = True
            stop_button.icon_color = ft.Colors.GREY_500
        else:
            play_button.disabled = True
            play_button.icon_color = ft.Colors.GREY_500
            stop_button.disabled = False
            stop_button.icon_color = ft.Colors.GREEN_300

        self._buttons_toggled = not(self._buttons_toggled)

        self._page.update()

    def update_timer_page_time(self, minutes, seconds):
        new_time = (f"{minutes:02d}:{seconds:02d}")
        self._set_timer_text(new_time)
        self._page.update()
    
    def timer_finished(self):
        if self._timer.in_productive_mode:
            self._db.add_session(self._POMODORO, self._CURRENT_SUBJECT, self._timer.get_start_time())
        self._set_timer_text("Done!")