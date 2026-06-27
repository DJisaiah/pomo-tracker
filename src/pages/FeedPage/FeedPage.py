from __future__ import annotations
from typing import Callable, TYPE_CHECKING
import flet as ft
from pages.FeedPage.FeedCard import FeedCard
from datetime import datetime

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
        self._feed = ft.Column(spacing=40)
        self._page_layout = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(height=10),
                    self._feed,
                    ft.Container(height=40)
                ],
                width=600,
                height=500,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.HIDDEN
            ),
            border_radius=ft.BorderRadius.all(6),
            border=ft.Border.all(
                width=2,
                color=ft.Colors.GREY_900
            )
        )
        self.get_feed()

    def _relative_time(self, time_str: str) -> str:
        time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        
        time_delta = now - time
        seconds = int(time_delta.total_seconds())

        if seconds < 60:
            return "just now"

        intervals = [
            (31536000, "years ago"),
            (2629800, "months ago"),
            (604800, "weeks ago"),
            (86400, "days ago"),
            (3600, "hours ago"),
            (60, "minutes ago")  
        ]

        for interval, timeframe in intervals:
            timeframe_time = seconds // interval
            if timeframe_time:
                return f"{timeframe_time} {timeframe}"

    def get_feed(self, e: ft.ControlEvent = None) -> None:
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
            start_time: str = self._relative_time(session[2])
            hours = duration_seconds // 3600
            minutes = (duration_seconds % 3600) // 60
            if hours:
                if minutes:
                    duration = f"{hours}h{minutes}m"
                else:
                    duration = f"{hours}h"
            else:
                    duration = f"{minutes}m"
            session_card = FeedCard(subject_name, duration, start_time)
            self._feed.controls.append(session_card)

    def get_page(self):
        return self._page_layout
