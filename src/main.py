import flet as ft

def main(page: ft.Page):
    page.title = "Pomo-Tracker"

    page.add(
        pages_nav_bar
    )

ft.app(main)
