import sys

import flet as ft

from components.composite import CustomWindowHeader
from components.composite.PagesNavBar import PagesNavBar
from core.DBManager import DBManager
from core.enums import StyleTokens
from core.PomoUtils import PomoUtils
from pages.FeedPage import FeedPage
from pages.StatsPage import StatsPage
from pages.TimerPage import TimerPage

WINDOW_TITLE = "Pomo-Tracker"
WINDOW_SIZE = 600
WINDOW_BG_COLOR = "#0A0A0B"
WINDOW_THEME = ft.ThemeMode.DARK


def main(page: ft.Page):
    load_app_settings(page)
    verify_integrity(page)


def verify_integrity(page: ft.Page):
    page.clean()
    # this will form part of adding user details
    platform = page.platform
    if platform is None:
        sys.exit()
    db: DBManager = DBManager()
    utilities: PomoUtils = PomoUtils(page, db, platform.is_mobile())

    def start_app():
        page.clean()
        setup_pages(page, utilities, db)
        page.update()

    continue_btn = ft.TextButton(
        content=ft.Text("Continue", color=ft.Colors.BLACK, font_family="Inter-Bold"),
        on_click=lambda _: start_app(),
        style=ft.ButtonStyle(
            bgcolor=StyleTokens.POMO_GREEN.value,
            overlay_color=ft.Colors.GREEN_300,
        ),
    )

    if utilities.check_data_integrity():
        start_app()
        return

    page.add(
        ft.Container(content=continue_btn, alignment=ft.Alignment.CENTER, expand=True)
    )
    page.update()


def setup_pages(page: ft.Page, utilities: PomoUtils, db: DBManager):
    timer_page: TimerPage = TimerPage(utilities)
    stats_page: StatsPage = StatsPage(utilities)
    feed_page: FeedPage = FeedPage(utilities)
    pages_nav_bar: PagesNavBar = PagesNavBar(
        {
            "Timer": ft.Icon(ft.Icons.HOURGLASS_TOP, color=ft.Colors.WHITE_70),
            "Stats": ft.Icon(ft.Icons.LEADERBOARD, color=ft.Colors.WHITE_70),
            "Feed": ft.Icon(ft.Icons.SUBJECT, color=ft.Colors.WHITE_70),
        },
        [timer_page, stats_page, feed_page],
    )

    if utilities.mobile_mode():
        page.run_task(
            page.set_allowed_device_orientations,
            [
                ft.DeviceOrientation.PORTRAIT_UP,
                ft.DeviceOrientation.PORTRAIT_DOWN,
            ],
        )

        page.navigation_bar, view_container = pages_nav_bar.get_nav_bar(True)
        page.add(
            ft.SafeArea(
                content=ft.Column(
                    controls=[
                        CustomWindowHeader.MobileWindowHeader(),
                        view_container,
                    ]
                ),
                expand=True,
            )
        )
    else:
        page.add(
            CustomWindowHeader.DesktopWindowHeader(), pages_nav_bar.get_nav_bar(False)
        )
    page.update()


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

    page.fonts = {
        "Space Grotesk": "fonts/SpaceGrotesk-Bold.ttf",
        "Space Grotesk-Regular": "fonts/SpaceGrotesk-Regular.ttf",
        "JetBrains Mono": "fonts/JetBrainsMono-Medium.ttf",
        "Inter": "fonts/Inter_18pt-Regular.ttf",
        "Inter-Bold": "fonts/Inter_18pt-Bold.ttf",
    }

    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            thumb_visibility=True,
            thumb_color=ft.Colors.GREY_800,
            track_color=ft.Colors.GREY_800,
            track_border_color=ft.Colors.GREY_800,
            thickness=4,
        ),
        font_family="Inter",
    )


ft.run(main, assets_dir="assets")
