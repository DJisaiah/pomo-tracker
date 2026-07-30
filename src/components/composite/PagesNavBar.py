from __future__ import annotations

from typing import cast

import flet as ft


class PagesNavBar:
    def __init__(
        self,
        labels: dict[str, ft.Icon],
        views: list[ft.Control],
        mobile: bool,
        icons: list[str] | None = None,
    ):
        self._labels = labels
        self._views = views
        if mobile:
            self._view_container = ft.Container(
                animate=ft.Animation(
                    curve=ft.AnimationCurve.FAST_OUT_SLOWIN, duration=5000
                ),
                expand=True,
            )
            self._navbar = MobileNavigation(self)
        else:
            self._navbar = DesktopNavigation(self)
            self._view_container = None

    def get_nav_bar(
        self,
    ) -> tuple[MobileNavigation, ft.Container] | DesktopNavigation:
        if self._view_container:
            return (cast(MobileNavigation, self._navbar), self._view_container)
        return cast(DesktopNavigation, self._navbar)

    def _on_tab_change(self, index: int) -> None:
        selected_view = self._views[index]
        refresh_fn = getattr(selected_view, "refresh", None)
        if callable(refresh_fn):
            refresh_fn()


class DesktopNavigation(ft.Tabs):
    def __init__(self, controller: PagesNavBar):
        tabs = ft.TabBar(
            tabs=[ft.Tab(label=tab_label) for tab_label in controller._labels],
            tab_alignment=ft.TabAlignment.CENTER,
            divider_color=ft.Colors.TRANSPARENT,
            indicator_color=ft.Colors.TRANSPARENT,
            overlay_color=ft.Colors.TRANSPARENT,
            label_text_style=ft.TextStyle(
                color=ft.Colors.WHITE,
                size=30,
                weight=ft.FontWeight.BOLD,
                font_family="Space Grotesk",
            ),
            unselected_label_text_style=ft.TextStyle(
                color=ft.Colors.GREY_700,
                size=15,
            ),
        )

        tab_views = ft.TabBarView(
            expand=True,
            controls=[ft.Column(controls=[tab_view]) for tab_view in controller._views],
        )

        super().__init__(
            selected_index=0,
            length=3,
            animation_duration=300,
            content=ft.Column(controls=[tabs, tab_views]),
            on_change=lambda e: controller._on_tab_change(cast(int, e.data)),
        )


class MobileNavigation(ft.NavigationBar):
    def __init__(self, controller: PagesNavBar):
        self._controller = controller
        self._vc = cast(ft.Container, self._controller._view_container)

        super().__init__(
            bgcolor=ft.Colors.TRANSPARENT,
            elevation=0,
            indicator_color="#7ED957",
            overlay_color=ft.Colors.TRANSPARENT,
            animation_duration=300,
            selected_index=0,
            destinations=[
                ft.NavigationBarDestination(icon=icon, label=label)
                for label, icon in controller._labels.items()
            ],
            on_change=self._switch_views,
        )
        self._init_views()

    def _init_views(self) -> None:
        self._vc.content = self._controller._views[0]

    def _switch_views(self, e: ft.ControlEvent | None = None):
        selected_view = self._controller._views[self.selected_index]
        self._vc.content = selected_view
