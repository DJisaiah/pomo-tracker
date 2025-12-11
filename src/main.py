import flet as ft
from pages_nav_bar import load_nav_bar_and_pages
from database.local_db import LocalDB
from pages.TimerPage.TimerPage import TimerPage
from pages.StatsPage.StatsPage import StatsPage
from core.PomoUtilities import PomoUtilities


def main(page: ft.Page):
    load_app_settings(page)
    create_db_and_pages(page)

def create_db_and_pages(page):
    utilities = PomoUtilities(page)
    #utilities.start_RPC()
    db = LocalDB()
    timer_page = TimerPage(utilities, db)
    stats_page = StatsPage(utilities, db)

    page.add(
        load_nav_bar_and_pages(
            timer_page,
            stats_page
        )
    )

def load_app_settings(page):
    page.title = "Pomo-Tracker"

    # window dimensions
    page.window.width = 600
    page.window.height = 600
    page.window.max_width = 600
    page.window.max_height = 600
    page.window.min_width = 600
    page.window.min_height = 600
    #page.padding = 10

    # colors
    page.bgcolor = ft.Colors.BLACK

    # mods
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            thumb_color=ft.Colors.TRANSPARENT,
            track_color=ft.Colors.TRANSPARENT,
            track_border_color=ft.Colors.TRANSPARENT
        )
    )                                                        


ft.app(main, assets_dir="assets")
