from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import flet as ft

from components.base.IslandContainer import IslandContainer
from components.composite.FeedCard import FeedCard
from core.enums import SubjectIcons, SubjectType

if TYPE_CHECKING:
    from core.DBManager import DBManager
    from core.PomoUtils import PomoUtils


class FeedPage:
    def __init__(self, utilities: PomoUtils):
        self._utilities = utilities
        self._db: DBManager = self._utilities.get_db()
        self._feed_empty: bool = True
        self._session_index = 0
        self._number_of_sessions = 10
        self._feed = ft.Column(spacing=40)
        self._feed_container = IslandContainer(self._feed, 450, 535)
        self._feed_container.padding = ft.Padding.symmetric(vertical=10)

        self._page_layout = ft.Column(
            controls=[ft.Container(), self._feed_container, ft.Container(height=20)],
            width=600,
            height=500,
            scroll=ft.ScrollMode.HIDDEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self._empty_feed_msg = ft.Column(
            controls=[
                ft.Text(
                    "Feed is empty",
                    color=ft.Colors.GREY_600,
                    weight=ft.FontWeight.W_600,
                ),
                ft.Text(
                    "When you or your friends have activity it'll show up here",
                    color=ft.Colors.GREY_700,
                    weight=ft.FontWeight.W_300,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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
            (60, "minutes ago"),
            (1, "seconds ago"),
        ]

        for interval, timeframe in intervals:
            timeframe_time = seconds // interval
            if timeframe_time:
                return f"{timeframe_time} {timeframe}"
        return "who knows when"

    def get_feed(self, e: ft.ControlEvent | None = None) -> None:
        # fetch/store sessions for the day from db
        sessions = self._db.get_sessions(self._number_of_sessions, self._session_index)
        self._session_index += 10

        # create/store session cards
        if not sessions and not self._feed.controls:
            self._feed.controls.append(self._empty_feed_msg)
            self._feed.alignment = ft.MainAxisAlignment.CENTER
            return
        elif sessions and self._feed_empty:
            self._feed_empty = False
            self._feed.alignment = ft.MainAxisAlignment.START
            self._feed.controls.clear()

        for session in sessions:
            subject_name: str = session[0]
            duration_seconds: int = session[1]
            start_time: str = self._relative_time(session[2])
            subject_type: str = SubjectType[session[3]].type_label
            subject_image: str = SubjectIcons[session[4]]
            hours = duration_seconds // 3600
            minutes = (duration_seconds % 3600) // 60
            if hours:
                if minutes:
                    duration = f"{hours}h{minutes}m"
                else:
                    duration = f"{hours}h"
            else:
                if not minutes:
                    duration = f"{int(duration_seconds)}s"
                else:
                    duration = f"{minutes}m"
            session_card = FeedCard(
                subject_name, duration, start_time, subject_type, subject_image
            )
            self._feed.controls.append(session_card)

        if len(self._feed.controls) >= 3:
            self._feed_container.height = None
        else:
            self._feed_container.height = 450
        self._utilities.update_page()

    def get_page(self):
        return self._page_layout
