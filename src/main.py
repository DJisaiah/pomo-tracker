import flet as ft
from pages_nav_bar import load_nav_bar_and_pages

def main(page: ft.Page):
    page.title = "Pomo-Tracker"

    page.add(
        load_nav_bar_and_pages(page)
    )

ft.app(main)

""" 
need to fix productivity bar and break bar being too far away
will probably have to put into column with timer text
will involve changing some other things..
"""