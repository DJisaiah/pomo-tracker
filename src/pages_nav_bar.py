import flet as ft
from timer_page import TimerPage

def load_nav_bar_and_pages(page):
    # initialise pages and reqs
    timer_screen = TimerPage(page)

    nav_bar = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Timer",
                content=ft.Column(controls=[timer_screen.get_page()])
            ),
            ft.Tab(
                text="Stats",
                content=ft.Text("", size=100)
            ),
            ft.Tab(
                text="Rankings",
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