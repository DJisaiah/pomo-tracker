import flet as ft

class GraphTracker:
    def __init__(self):
        self._graph = ft.BarChart(
            bar_groups=[
                ft.BarChartGroup(
                    x=0,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=40,
                            width=40,
                            color=ft.Colors.GREEN,
                            # tooltip="Apple",
                            border_radius=0,
                        ),
                    ],
                ),
            ],
            border=ft.border.all(1, ft.Colors.GREY_400),
            left_axis=ft.ChartAxis(
                labels_size=10, title=ft.Text("Fruit supply"), title_size=10
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=0, label=ft.Container(ft.Text("Apple"), padding=10)
                    ),
                    ft.ChartAxisLabel(
                        value=1, label=ft.Container(ft.Text("Blueberry"), padding=10)
                    ),
                    ft.ChartAxisLabel(
                        value=2, label=ft.Container(ft.Text("Cherry"), padding=10)
                    ),
                    ft.ChartAxisLabel(
                        value=3, label=ft.Container(ft.Text("Orange"), padding=10)
                    ),
                ],
                labels_size=10,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.Colors.GREY_300, width=1, dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREY_300),
            max_y=60,
            interactive=True
        )

    def get_graph(self):
        return ft.Container(
            content=self._graph,
            height=400,
            width=550
        )