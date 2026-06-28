from __future__ import annotations
from typing import TYPE_CHECKING
import flet as ft
import flet_charts as fch
from datetime import datetime


class GraphTracker:
    def __init__(self, db: LocalDB, refresh_graph):
        self._db: LocalDB = db
        self._refresh_graph = refresh_graph
        self._bar_groups = []
        self._bottom_axis_labels = []
        self._time_scale = None
        self._max_y = 0
        self._min_graph_width = 600

        # controls
        self._graph = fch.BarChart(
            group_alignment=ft.MainAxisAlignment.SPACE_AROUND,
            left_axis=fch.ChartAxis(
                label_size=25,
                labels=[fch.ChartAxisLabel(
                    value=v, label=ft.Text("", weight=ft.FontWeight.BOLD)
                )
                for v in range(1, 11, 2)
                ]
            ),
            horizontal_grid_lines=fch.ChartGridLines(
                color=ft.Colors.GREY_800,
                width=1
            ),
            #tooltip_bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREY_800),
            tooltip=fch.BarChartTooltip(
                bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREY_800),
                direction=fch.BarChartTooltipDirection.TOP,
                horizontal_offset=-30,
                fit_inside_vertically=True
            ),
            max_y=0,
            min_y=0,
            interactive=True,
            )

        self._graph_container = ft.Container(
            content=self._graph,
            height=400,
            width=500,
            padding=ft.Padding.symmetric(vertical=10, horizontal=10)
        )


        self._GraphTracker_container = ft.Container(
            height=70,
            content=ft.Column(controls=[
                ft.Row(controls=[
                    ft.Text("SUBJECT HOURS", size=14,
                        text_align=ft.TextAlign.LEFT,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_700
                    ),
                    ft.Dropdown(
                        bgcolor=ft.Colors.BLACK_87,
                        color=ft.Colors.WHITE_70,
                        editable=False,
                        label=ft.Text(
                            "Select a Time Scale!",
                            color=ft.Colors.WHITE_70
                        ),
                        border_color=ft.Colors.GREY_800,
                        width=220,
                        on_select=self._change_time_scale,
                        options=[
                            ft.DropdownOption(
                                key="Day",
                                content=ft.Text("Day", color=ft.Colors.WHITE_70)
                            ),
                            ft.DropdownOption(
                                key="Week",
                                content=ft.Text("Week", color=ft.Colors.WHITE_70)
                            ),
                            ft.DropdownOption(
                                key="Month",
                                content=ft.Text("Month", color=ft.Colors.WHITE_70)
                            ),
                            ft.DropdownOption(
                                key="Year",
                                content=ft.Text("Year", color=ft.Colors.WHITE_70)
                            )
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.Row(
                    controls=[self._graph_container],
                    scroll=ft.ScrollMode.ALWAYS,
                    expand=True
                )
            ], 
            expand=True),
            padding=ft.Padding.symmetric(vertical=10, horizontal=10),
            width=530,
            #bgcolor=ft.Colors.GREY_900,
            bgcolor=ft.Colors.BLACK_87,
            border_radius=ft.BorderRadius.all(6),
            border=ft.Border.all(
                width=2,
                color=ft.Colors.GREY_900
                    )
        )

    def _render_graph(self, scale: str) -> None:
        self._max_y = 0
        self._bar_groups.clear()
        self._bottom_axis_labels.clear()
        self._subject_seconds_dict = self._db.get_all_subject_seconds(scale)
        index=1
        for subject, seconds in self._subject_seconds_dict.items():
            index+=1
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            self._max_y = max(self._max_y, hours)
            self._bar_groups.append(
                fch.BarChartGroup(
                    x=index,
                    rods=[
                        fch.BarChartRod(
                                from_y=0,
                                to_y=hours,
                                tooltip=fch.BarChartRodTooltip(f"{hours}h{minutes}m"),
                                border_radius=2,
                                width=30,
                                color=ft.Colors.GREEN
                            )
                    ]
                )
            )
            self._bottom_axis_labels.append(
                    fch.ChartAxisLabel(
                        value=index,
                        label=ft.Container(
                            ft.Text(
                                f"{subject}",
                                color=ft.Colors.WHITE,
                                size=11
                            )
                        )
                    )
            )
        self._graph.groups = self._bar_groups
        self._graph.bottom_axis = fch.ChartAxis(
            labels=self._bottom_axis_labels,
            label_size=20
            )
        self._graph_container.width = max(self._min_graph_width, index * 130)

    def _render_graph_scale(self, scale: str) -> int:
        max_scale = self._max_y
        self._graph.left_axis = fch.ChartAxis(
                label_size=30,
                labels=[fch.ChartAxisLabel(
                    value=v, 
                    label=ft.Text(
                        f"{v:01d} ",
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.WHITE
                    )
                )
                for v in range(0, max_scale + 5, 2)
                ]
            )
        self._graph.max_y = max_scale + 5


    def _change_time_scale(self, e: ft.ControlEvent) -> None:
        # gracktracker full size from initial
        self._GraphTracker_container.height = None
        scale = e.control.value
        if scale == "Year":
            self._render_graph("Y")
        elif scale == "Month":
            self._render_graph("M")
        elif scale == "Week":
            self._render_graph("W")
        elif scale == "Day":
            self._render_graph("D")
        self._render_graph_scale(scale[0]) 
        self._GraphTracker_container.update()
        self._graph.update()

    def get_graph(self) -> ft.Container:
        return self._GraphTracker_container
