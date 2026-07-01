import flet as ft

import core.DesignLanguage as ui
from core.PomoUtilities import PomoUtilities
from core.DatabaseManager import DatabaseManager
from pages.FeedPage import FeedPage
from pages.StatsPage import StatsPage
from pages.TimerPage import TimerPage
from components.composite.PagesNavBar import PagesNavBar


WINDOW_TITLE = "Pomo-Tracker"
WINDOW_SIZE = 600
WINDOW_BG_COLOR = ft.Colors.BLACK
WINDOW_THEME = ft.ThemeMode.DARK


def main(page: ft.Page):
    load_app_settings(page)
    create_db_and_pages(page)

def create_db_and_pages(page: ft.Page):
    db: DatabaseManager = DatabaseManager()
    utilities: PomoUtilities = PomoUtilities(page, db)
    timer_page: TimerPage = TimerPage(utilities)
    stats_page: StatsPage = StatsPage(utilities)
    feed_page: FeedPage = FeedPage(utilities)
    pages_nav_bar: PagesNavBar = PagesNavBar(
        ["Timer Page", "Stats Page", "Feed Page"],
        [timer_page, stats_page, feed_page]
    )

    page.add(
        ui.get_window_header(page),
        pages_nav_bar
    )

def load_app_settings(page: ft.Page):
    page.title = "Pomo-Tracker"

    # window dimensions
    page.window.width = WINDOW_SIZE
    page.window.height = WINDOW_SIZE
    page.window.max_width = WINDOW_SIZE
    page.window.max_height = WINDOW_SIZE
    page.window.min_width = WINDOW_SIZE
    page.window.min_height = WINDOW_SIZE

    # colors
    page.bgcolor = WINDOW_BG_COLOR
    page.theme_mode = WINDOW_THEME
    page.window.title_bar_hidden = True

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
