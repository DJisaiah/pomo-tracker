from enum import Enum, StrEnum

import flet as ft


class SubjectIcons(StrEnum):
    AROUND_THE_WORLD = "undraw_travel-everywhere_sxzj.svg"
    TAKING_NOTES = "undraw_taking-notes_oyqz.svg"
    STUDYING_SCIENCE = "undraw_studying-science_kk9e.svg"
    STARS = "undraw_stars_5pgw.svg"
    PUZZLE_SOLVED = "undraw_puzzle-solved_qdjq.svg"
    MEDITATION = "undraw_meditation_k4oa.svg"
    MATHEMATICS = "undraw_mathematics_0j2b.svg"
    MATH = "undraw_math_ldpv.svg"
    MAKING_ART = "undraw_making-art_c05m.svg"
    LEARNING_TO_SKETCH = "undraw_learning-to-sketch_uaxi.svg"
    FOCUSED = "undraw_focused_m9bj.svg"
    DATA_AT_WORK = "undraw_data-at-work_3tbf.svg"
    DANCE_WORKOUT = "undraw_dance-workout_sowy.svg"
    BOOK_LOVER = "undraw_book-lover_m9n3.svg"
    BLOGGING = "undraw_blogging_38kl.svg"


class SubjectType(Enum):
    STUDY_TYPE = ("1", "Studying")
    CODE_TYPE = ("2", "Coding")
    PRAC_TYPE = ("3", "Practicing")
    WORKING_TYPE = ("4", "Working on")

    def __init__(self, type_id: str, type_label: str):
        self.type_id = type_id
        self.type_label = type_label

    @classmethod
    def from_id(cls, type_id: str) -> str:
        type_id = str(type_id)
        for member in cls:
            if member.type_id == type_id:
                return member.name
        return ""


class StyleTokens(Enum):
    RADIUS_SMALL = 6
    BORDER_THICKNESS = 2
    BORDER_COLOR = ft.Colors.GREY_900
