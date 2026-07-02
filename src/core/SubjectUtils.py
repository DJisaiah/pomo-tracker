from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from components.composite.SubjectEditor import SubjectEditor
from core.enums import SubjectIcons, SubjectType

if TYPE_CHECKING:
    import flet as ft

    from core.DBManager import DBManager
    from core.PomoUtils import PomoUtils


class SubjectUtils:
    def __init__(
        self,
        utilities: PomoUtils,
    ):
        """methods relating to subjects and manipulating them

        allows controls to add/edit subjects and check their validity

        Args:
            utilities: shared instance of PomoUtils
        """
        self._utilities: PomoUtils = utilities
        self._db: DBManager = self._utilities.get_db()
        self._current_subject: str | None = None
        self._actions = SubjectActions(
            self.edit_subject,
            self.add_subject,
            self.remove_subject,
            self.get_all_subjects,
            self.get_current_subject,
            self.update_current_subject,
            self.check_subjects
        )

    def get_actions(self):
        return self._actions

    def check_subjects(self):
        subjects_info = self._db.get_subjects_info()
        for subject in subjects_info:
            subject_id, subject_name, subject_type, subject_image = subject
            if not subject_type or not subject_image:
                self.edit_subject(subject_name)
                self._utilities.alert_user(
                    "Missing Subject Data!",
                    f"You're missing subject type/image for \n{subject_name}!"
                )

    def update_current_subject(self, subject_name: str | None = None) -> None:
        if subject_name is None:
            self._current_subject = None
            return
        self._current_subject = subject_name

    def get_current_subject(self) -> str:
        return self._current_subject if self._current_subject else ""

    def get_current_subject_type(self) -> str:
        return "some subject" #TODO

    def _valid_subject(self, usr_subject_name: str) -> bool:
        # check subject is not a duplicate
        if usr_subject_name.strip(" ") == "":
            self._utilities.alert_user(
                "Invalid Subject", "Subject name can't be empty."
            )
            return False
        subjects = self._db.get_all_subjects()
        for subject_id, subject_name in subjects:
            subject_text = usr_subject_name
            if subject_text == subject_name:
                self._utilities.alert_user("Invalid Subject", "Subject already exists.")
                return False
        return True

    def _send_subject_to_db(self,
        e: ft.ControlEvent,
        response: list[str]
    ) -> None:
        subject_name: str = response[1]
        subject_type: str = SubjectType.from_id(response[2])
        subject_image: str = SubjectIcons(response[3]).name

        if not self._valid_subject(subject_name):
            return
        self._db.add_subject(subject_name, subject_type, subject_image)
        self._utilities.close_dialog()
        self._utilities.text_toast("Subject Added!")

    def get_all_subjects(self) -> list[tuple[int, str]]:
        all_subjects: list[tuple[int, str]] = self._db.get_all_subjects()
        return all_subjects

    def add_subject(self) -> None:
        self._utilities.show_dialog(SubjectEditor(self._send_subject_to_db))

    def remove_subject(self, subject_name: str) -> None:
        self._db.remove_subject(subject_name)

    def _edit_subject(self,
        e: ft.ControlEvent,
        response: list[str]
    ) -> None:
        old_subj, new_subj, subj_type, subj_image = response
        self._db.update_subject(
            old_subj,
            new_subj,
            subj_type,
            subj_image
        )
        self._utilities.close_dialog()
        self._utilities.text_toast("Subject Updated!")

    def edit_subject(self, subject_name: str) -> None:
        self._utilities.show_dialog(
            SubjectEditor(
                self._edit_subject,
                subject_name
             )
        )

@dataclass
class SubjectActions:
    edit: Callable[[str], None]
    add: Callable[[], None]
    remove: Callable[[str], None]
    get_all: Callable[[], list[tuple[int, str]]]
    current_subject: Callable[[], str]
    update_subject: Callable[[str | None], None]
    check_subjects: Callable[[], None]
