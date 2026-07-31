from __future__ import annotations

from math import pi
from typing import TYPE_CHECKING

import flet as ft
import flet_charts as fch

from components.base.EnhancedCupertinoSlidingSegementedButton import (
    EnhancedCupertinoSlidingSegmentedButton,
)
from core.enums import StyleTokens

if TYPE_CHECKING:
    from core.DBManager import DBManager


class SubjectTrackingGraph(ft.Column):
    def __init__(self, db: DBManager, mobile: bool):
        super().__init__(expand=True, spacing=4)
        self._db: DBManager = db
        self._mobile = mobile
        self._bar_groups: list[fch.BarChartGroup] = []
        self._bottom_axis_labels: list[fch.ChartAxisLabel] = []
        self._max_y = 0

        self._graph = fch.BarChart(
            group_alignment=ft.MainAxisAlignment.SPACE_AROUND,
            max_y=0,
            min_y=0,
            interactive=False,
        )

        self._graph_container = ft.Column(
            controls=[self._graph], width=200, rotate=ft.Rotate(angle=pi / 2)
        )

        self._subjects_col = ft.Column(
            spacing=10 if self._mobile else 5, width=110 if self._mobile else None
        )
        self._subject_hr_col = ft.Column(spacing=14 if self._mobile else 10)

        self._scale = EnhancedCupertinoSlidingSegmentedButton(
            labels=[
                ft.Text("Day", color=ft.Colors.WHITE, weight=ft.FontWeight.W_700),
                ft.Text("Week", color=ft.Colors.WHITE, weight=ft.FontWeight.W_700),
                ft.Text("Month", color=ft.Colors.WHITE, weight=ft.FontWeight.W_700),
                ft.Text("Year", color=ft.Colors.WHITE, weight=ft.FontWeight.W_700),
            ],
            colors=[StyleTokens.POMO_GREEN.value for i in range(4)],
            actions=[
                lambda: self._change_time_scale("Day"),
                lambda: self._change_time_scale("Week"),
                lambda: self._change_time_scale("Month"),
                lambda: self._change_time_scale("Year"),
            ],
            selected_index=3,
        )

        self.controls = [
            ft.Row(
                controls=[self._scale],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    self._subjects_col,
                    self._graph_container,
                    self._subject_hr_col,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
        ]

    def did_mount(self):
        self._render_graph("Y")
        self._render_graph_scale("Y")
        self._graph.update()
        self.update()

    def _render_graph(self, scale: str) -> None:
        self._max_y = 0
        self._bar_groups.clear()
        self._subjects_col.controls.clear()
        self._subject_hr_col.controls.clear()
        self._subject_seconds_dict = self._db.get_all_subject_seconds(scale)
        rods: list[fch.BarChartRod] = []
        self._bar_groups.append(
            fch.BarChartGroup(
                x=0,
                rods=rods,
            )
        )

        def trunc_subject(s: str) -> str:
            nonlocal self
            if self._mobile and len(s) >= 7:
                return f"{s[:7]}..."
            elif len(s) >= 14:
                return f"{s[14:]}..."
            return s

        index = 1
        for subject, seconds in self._subject_seconds_dict.items():
            index += 1
            hours_f = seconds / 3600
            minutes_f = (seconds % 3600) // 60
            hours = int(hours_f)
            minutes = int(minutes_f)
            if not hours and not minutes:
                formatted_time = f"{seconds}s"
            else:
                formatted_time = f"{hours}h{minutes}m"
            self._max_y = max(self._max_y, hours)
            rods.append(
                fch.BarChartRod(
                    from_y=0,
                    to_y=hours_f,
                    border_radius=2,
                    width=24,
                    color=ft.Colors.GREEN,
                    gradient=ft.LinearGradient(["#9AE87A", "#7ED957"]),
                )
            )

            self._subjects_col.controls.append(
                ft.Text(
                    trunc_subject(subject),
                    color=ft.Colors.WHITE,
                    size=11 if self._mobile else 15,
                    weight=ft.FontWeight.W_600,
                )
            )

            self._subject_hr_col.controls.append(
                ft.Text(
                    formatted_time,
                    color=ft.Colors.GREY_600,
                    size=9 if self._mobile else 12,
                )
            )

        self._graph.groups = self._bar_groups

    def _render_graph_scale(self, scale: str) -> None:
        max_scale = self._max_y
        self._graph.max_y = max_scale + 5

    def _change_time_scale(self, scale: str) -> None:
        self.height = None
        if scale == "Year":
            self._render_graph("Y")
        elif scale == "Month":
            self._render_graph("M")
        elif scale == "Week":
            self._render_graph("W")
        elif scale == "Day":
            self._render_graph("D")
        self._render_graph_scale(scale[0])
        self._graph.update()
        self.update()
