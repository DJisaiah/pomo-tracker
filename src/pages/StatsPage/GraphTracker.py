import flet as ft
from datetime import datetime


class GraphTracker:
    def __init__(self, db):
        self._db = db
        self._bar_groups = []
        self._bottom_axis_labels = []
        self._time_scale = None
        self._graph = ft.BarChart(
            left_axis=ft.ChartAxis(
                labels_size=30,
                labels=[ft.ChartAxisLabel(
                    value=v, label=ft.Text(f"{v}")
                )
                for v in range(0, 21, 5)
                ]
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.Colors.GREY_800,
                width=1
            ),
            tooltip_bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREY_800),
            max_y=20,
            min_y=0,
            interactive=True
            )
        self._graph_container = ft.Container(
            content=ft.Column(controls=[
                ft.Row(controls=[
                    ft.Text("Subject Hours", size=20, text_align=ft.TextAlign.LEFT, weight=ft.FontWeight.BOLD),
                    ft.Dropdown(
                        editable=False,
                        label="Select a Time Scale!",
                        border_color=ft.Colors.WHITE70,
                        width=220,
                        on_change=self._change_time_scale,
                        options=[
                            ft.DropdownOption(
                                key="Day",
                                content=ft.Text("Day")
                            ),
                            ft.DropdownOption(
                                key="Week",
                                content=ft.Text("Week")
                            ),
                            ft.DropdownOption(
                                key="Month",
                                content=ft.Text("Month")
                            ),
                            ft.DropdownOption(
                                key="Year",
                                content=ft.Text("Year")
                            )
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                self._graph
            ], 
            spacing=20,
            expand=True),
            padding=ft.padding.symmetric(vertical=10, horizontal=10),
            width=530,
            bgcolor=ft.Colors.GREY_900,
            border_radius=ft.border_radius.all(6)
        )

    def _render_graph(self, month=None, day=None, week=False):
        self._graph.bar_groups.clear()
        self._graph.bottom_axis = None
        self._subject_seconds_dict = self._db.get_all_subject_seconds(month, day, week)
        i=-1
        for subject, seconds in self._subject_seconds_dict.items():
            i+=1
            hours = seconds / 3600
            minutes = seconds % 3600
            print("hours found", hours, "subject is:", subject)
            self._bar_groups.append(
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                                from_y=0,
                                to_y=hours,
                                tooltip=round(hours, 2),
                                border_radius=2,
                                width=30,
                                color=ft.Colors.GREEN
                            )
                    ]
                    )
                )
            self._bottom_axis_labels.append(
                    ft.ChartAxisLabel(
                        value=i, label=ft.Container(ft.Text(f"{subject}", color=ft.Colors.WHITE))
                        )
                )
        self._graph.bar_groups = self._bar_groups
        self._graph.bottom_axis = ft.ChartAxis(
            labels=self._bottom_axis_labels,
            labels_size=20
            )

    def _change_time_scale(self, e):
        scale = e.control.value
        if scale == "Year":
            self._render_graph()
        elif scale == "Month":
            self._render_graph(datetime.now().month)
        elif scale == "Week":
            self._render_graph(None, None, True)
        elif scale == "Day":
            self._render_graph(datetime.now().month, datetime.now().day)
        self._graph_container.update()

    def get_graph(self):
        return self._graph_container