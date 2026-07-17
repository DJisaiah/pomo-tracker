from __future__ import annotations

import flet as ft


class PagesNavBar:
    def __init__(
        self,
        labels: list[str],
        views: list[ft.Control],
        mobile: bool,
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
    ) -> tuple[MobileNavigation | DesktopNavigation, ft.Container] | DesktopNavigation:
        if self._view_container:
            return (self._navbar, self._view_container)
        assert isinstance(self._navbar, DesktopNavigation)
        return self._navbar

    def _on_tab_change(self, index: int) -> None:
        selected_view = self._views[index]
        if hasattr(selected_view, "refresh"):
            selected_view.refresh()  # type: ignore


class DesktopNavigation(ft.Tabs):
    def __init__(self, controller: PagesNavBar):
        tabs = ft.TabBar(
            tabs=[ft.Tab(label=tab_label) for tab_label in controller._labels],
            tab_alignment=ft.TabAlignment.CENTER,
            divider_color=ft.Colors.TRANSPARENT,
            indicator_color=ft.Colors.TRANSPARENT,
            overlay_color=ft.Colors.TRANSPARENT,
            label_text_style=ft.TextStyle(
                color=ft.Colors.WHITE_70, size=30, weight=ft.FontWeight.BOLD
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
            on_change=lambda e: controller._on_tab_change(int(e.data)),  # type: ignore
        )


class MobileNavigation(ft.NavigationBar):
    def __init__(self, controller: PagesNavBar):
        self._controller = controller
        self._vc = self._controller._view_container

        super().__init__(
            bgcolor=ft.Colors.TRANSPARENT,
            indicator_color=ft.Colors.TRANSPARENT,
            overlay_color=ft.Colors.TRANSPARENT,
            animation_duration=300,
            selected_index=0,
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Text(
                        label,
                        weight=ft.FontWeight.BOLD,
                        animate_scale=ft.Animation(
                            curve=ft.AnimationCurve.FAST_LINEAR_TO_SLOW_EASE_IN,
                            duration=300,
                        ),
                    )
                )
                for label in controller._labels
            ],
            on_change=self._switch_views,  # type: ignore
        )
        self._init_views()

    def _init_views(self) -> None:
        assert isinstance(self._vc, ft.Container)
        self._vc.content = self._controller._views[0]
        text_control = self.destinations[0].icon
        assert isinstance(text_control, ft.Text)
        text_control.color = ft.Colors.GREEN_200
        text_control.scale = 3

    def _switch_views(self, e: ft.ControlEvent | None = None):
        self.index_animation()
        selected_view = self._controller._views[self.selected_index]
        self._vc.content = selected_view  # type: ignore
        assert isinstance(self._vc, ft.Container)
        self._vc.update()

    def index_animation(self) -> None:
        for index, view_label in enumerate(self.destinations):
            text_control = view_label.icon
            assert isinstance(text_control, ft.Text)
            if index == self.selected_index:
                text_control.color = ft.Colors.GREEN_200
                text_control.scale = 3
            else:
                text_control.color = ft.Colors.GREY_700
                text_control.scale = 1
            text_control.update()
