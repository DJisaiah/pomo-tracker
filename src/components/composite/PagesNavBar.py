import flet as ft


class PagesNavBar(ft.Tabs):
    """
    given labels and views, returns an animated navbar with said items
    """
    def __init__(
        self,
        labels: list[str],
        views: list[
            ft.Container |
            ft.Column |
            ft.Row
        ]
    ):
        tabs = ft.TabBar(
            tabs=[
                ft.Tab(label=tab_label) for tab_label in labels
            ],
            tab_alignment=ft.TabAlignment.CENTER,
            divider_color=ft.Colors.TRANSPARENT,
            indicator_color=ft.Colors.TRANSPARENT,
            overlay_color=ft.Colors.TRANSPARENT,
            label_text_style=ft.TextStyle(
                color=ft.Colors.WHITE_70,
                size=30,
                weight=ft.FontWeight.BOLD
            ),
            unselected_label_text_style=ft.TextStyle(
                color=ft.Colors.GREY_700,
                size=15,
            )
        )

        tab_views = ft.TabBarView(
            expand=True,
            controls=[
                ft.Column(controls=[tab_view]) for tab_view in views
            ]
        )

        super().__init__(
            selected_index=0,
            length=3,
            animation_duration=300,
            content=ft.Column(
                controls=[
                    tabs,
                    tab_views
                ]
            )
        )

