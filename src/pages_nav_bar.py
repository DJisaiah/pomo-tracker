import flet as ft
from timer_page import TimerPage

def load_nav_bar_and_pages(page):
    # initialise pages and reqs
    timer_screen = TimerPage(page)
    timer_text = timer_screen.get_timer_text()
    buttons = timer_screen.get_buttons()

    nav_bar = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Timer",
                content=ft.Column(controls=[timer_text, buttons])
            ),
            ft.Tab(
                text="Stats",
                content=ft.Text("Stats Section", size=100)
            ),
            ft.Tab(
                text="Rankings",
                content=ft.Text("Rankings Section", size=100)
            ),
            ft.Tab(
                text="Settings",
                content=ft.Text("Settings Section", size=100)
            )
        ],
        tab_alignment=ft.TabAlignment.CENTER
    )
    return nav_bar