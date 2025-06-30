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

    # 
    #page.window.bgcolor = ft.Colors.BLUE_GREY_50
    page.bgcolor = ft.Colors.BLACK

    page.add(
        load_nav_bar_and_pages(page)
    )

ft.app(main)
