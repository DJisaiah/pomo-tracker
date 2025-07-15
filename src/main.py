import flet as ft
from pages_nav_bar import load_nav_bar_and_pages

def main(page: ft.Page):
    page.title = "Pomo-Tracker"

    # window dimensions
    page.window.width = 600
    page.window.height = 600
    page.window.max_width = 600
    page.window.max_height = 600
    page.window.min_width = 600
    page.window.min_height = 600

    # colors
    page.bgcolor = ft.Colors.BLACK

    page.add(
        load_nav_bar_and_pages(page)
    )

ft.app(main)

"""
Todo:
- need to clean up timer page and modularise bits like classes for subject dropdown
    - input filter in flet is bugged for textfield in dropdown, so will need to do this manually until fixed
- create helper function for localdb for database operations DRY
    - also need to add check to add_subject in case subject is already in db
"""