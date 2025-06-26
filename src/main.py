import flet as ft
from pages_nav_bar import load_nav_bar_and_pages

def main(page: ft.Page):
    page.title = "Pomo-Tracker"

    page.add(
        load_nav_bar_and_pages(page)
    )

ft.app(main)

"""
BUG:
timer stop and start has glitching bug
probably due to page updates between toggle and start
"""
