import flet as ft

def load_nav_bar_and_pages(timer_page, stats_page):
    nav_bar = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Timer",
                content=ft.Column(controls=[timer_page.get_page()])
            ),
            ft.Tab(
                text="Stats",
                content=ft.Column(controls=[stats_page.get_page()])
            ),
            ft.Tab(
                text="Feed",
                content=ft.Text("", size=100)
            ),
            ft.Tab(
                text="Settings",
                content=ft.Text("", size=100)
            )
        ],
        tab_alignment=ft.TabAlignment.CENTER,
        divider_color=ft.Colors.BLUE_GREY_700,
        indicator_color=ft.Colors.LIGHT_GREEN_300,
        label_color=ft.Colors.LIGHT_GREEN_300
    )
    return nav_bar