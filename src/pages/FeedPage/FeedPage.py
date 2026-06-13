from __future__ import annotations
from typing import Callable, TYPE_CHECKING
import flet as ft
from pages.FeedPage.FeedCard import FeedCard

if TYPE_CHECKING:
    from core.PomoUtilities import PomoUtilities
    from database.local_db import LocalDB
    from pages.FeedPage.FeedCard import FeedCard


class FeedPage:
    def __init__(self, utilities: PomoUtilities):
        self._utilities = utilities
        self._db: LocalDB = self._utilities.get_db()
        self._session_index = 0
        self._number_of_sessions = 10
        self._feed = ft.Column()
        self._page_layout = ft.Column(
            controls=[
                ft.Container(height=10),
                self._feed,
                ft.Container(height=10)
            ]
        )


    def get_feed(self, e) -> list[FeedCard]:
        print("called")
        # fetch/store sessions for the day from db
        sessions = self._db.get_sessions(
            self._number_of_sessions,
            self._session_index
        )
        self._session_index += 10
        
        # create/store session cards
        for session in sessions:
            subject_name: str = session[0]
            duration_seconds: int = session[1]
            start_time: str = session[2]
            hours = duration_seconds / 3600
            minutes = duration_seconds % 3600

            duration = f"{hours:02d}h{minutes:02d}m"
            session_card = FeedCard(subject_name, duration, start_time)
            self._feed.append(session_card)

        # return list of feed

    def get_page(self):
        return self._page_layout
