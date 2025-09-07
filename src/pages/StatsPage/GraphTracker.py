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
                            to_y=10,
                            width=30,
                            color=ft.Colors.GREEN,
                            # tooltip="Apple",
                            border_radius=0,
                        ),
                    ],
                ),
            ],
            #border=ft.border.all(10, ft.Colors.GREY_400),
            left_axis=ft.ChartAxis(
                labels_size=30,
                labels=[ft.ChartAxisLabel(
                    value=v, label=ft.Text(f"{v}")
                )
                for v in range(0, 21, 5)

                ]
                
                #title=ft.Text("Fruit supply"),
                #title_size=20
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=0, label=ft.Container(ft.Text("Applied Math", color=ft.Colors.WHITE))
                    )
                    #ft.ChartAxisLabel(
                    #    value=1, label=ft.Container(ft.Text("Blueberry"), padding=10)
                    #),
                    #ft.ChartAxisLabel(
                    #    value=2, label=ft.Container(ft.Text("Cherry"), padding=10)
                    #),
                    #ft.ChartAxisLabel(
                    #    value=3, label=ft.Container(ft.Text("Orange"), padding=10)
                    #),
                ],
                labels_size=20,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.Colors.GREY_800,
                width=1
            ),
            tooltip_bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREY_300),
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

    def get_graph(self):
        return self._graph_container