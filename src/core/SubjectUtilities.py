from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from pages.TimerPage.SubjectEditor import SubjectEditor
from core.enums import SubjectIcons, SubjectType

if TYPE_CHECKING:
    from core.PomoUtilities import PomoUtilities
    from database.LocalDB import LocalDB


class SubjectUtilities:
    def __init__(
        self,
        utilities: PomoUtilities,
        subjects: dict,
        db: LocalDB,
        update_menu: Callable[None, None]
        
    ):
        self._utilities = utilities
        self._subjects = subjects
        self._db = db
        self._update_menu = update_menu

    def _valid_subject(self, subject_name: str) -> bool:
        # check subject is not a duplicate
        if subject_name.strip(" ") == "":
            self._utilities.alert_user("Invalid Subject", "Subject name can't be empty.")
            return False
        for subject in self._subjects:
            subject_text = subject.text
            if subject_text == subject_name:
                self._utilities.alert_user("Invalid Subject", "Subject already exists.")
                return False
        return True

    def _send_subject_to_db(self, 
        e: ft.ControlEvent,
        **kwargs
        ) -> None:

        subject_name = kwargs["subject_name"]
        subject_type = SubjectType.from_id(kwargs["subject_type"])
        subject_image = SubjectIcons(kwargs["subject_image"]).name       

        if not self._valid_subject(subject_name):
            return
        self._db.add_subject(subject_name, subject_type, subject_image)
        self._utilities.close_dialog()
        self._utilities.text_toast("Subject Added!")
        self._update_menu()

    def add_subject(self) -> None:
        self._utilities.show_dialog(SubjectEditor(self._send_subject_to_db))

    def _edit_subject(self,
        e: ft.ControlEvent,
        **kwargs
        ) -> None:
        new_subject_type = SubjectType.from_id(kwargs["subject_type"])
        new_subject_image = SubjectIcons(kwargs["subject_image"]).name
        self._db.update_subject(
            kwargs["subject_name"],
            kwargs["new_subject_name"],
            new_subject_type,
            new_subject_image
        )
        self._utilities.close_dialog()
        self._utilities.text_toast("Subject Updated!")
        self._update_menu()

    def edit_subject(self, subject_name: str) -> None:
        self._utilities.show_dialog(
            SubjectEditor(
                self._edit_subject,
                subject_name
             )
        )
