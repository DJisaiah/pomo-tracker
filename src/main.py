import flet as ft
from pages_nav_bar import load_nav_bar_and_pages
from database.local_db import LocalDB
from pages.TimerPage.TimerPage import TimerPage
from pages.StatsPage.StatsPage import StatsPage
from core.PomoUtilities import PomoUtilities


def main(page: ft.Page):
    load_app_settings(page)
    create_db_and_pages(page)

def create_db_and_pages(page: ft.Page):
    db: LocalDB = LocalDB()
    utilities: LocalDB = PomoUtilities(page, db)
    timer_page: TimerPage = TimerPage(utilities)
    stats_page: StatsPage = StatsPage(utilities)

    page.add(
        load_nav_bar_and_pages(
            timer_page,
            stats_page
        )
    )

def load_app_settings(page: ft.Page):
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

    # mods
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            thumb_color=ft.Colors.GREY_800,
            track_color=ft.Colors.GREY_800,
            track_border_color=ft.Colors.GREY_800,
            thickness=4
        )
    )                                                        


ft.run(main, assets_dir="assets")
