from typing import Callable, cast

import flet as ft


class EnhancedCupertinoSlidingSegmentedButton(ft.CupertinoSlidingSegmentedButton):
    def __init__(
        self,
        *,
        labels: list[ft.Text],  # strictly a text control
        colors: list[ft.ColorValue],
        actions: list[Callable[[], None]] | None = None,
        selected_index: int = 0,
    ):
        """adds dynamic thumb colors and custom actions on select to control"""
        super().__init__(
            controls=labels,  # type: ignore
            selected_index=selected_index,
            on_change=self._on_change,
        )
        self._colors = colors
        self._actions = actions

        def init():
            nonlocal colors, self
            self.thumb_color = colors[self.selected_index]
            self._toggle_colors()

        init()

    def reset(self):
        self.selected_index = 0
        self._on_change()

    def _toggle_colors(self) -> None:
        for index, control in enumerate(self.controls):
            c = cast(ft.Text, control)
            if index == self.selected_index:
                c.color = ft.Colors.BLACK
                c.weight = ft.FontWeight.W_600
                continue
            c.color = None
            c.weight = ft.FontWeight.W_400

    def _on_change(
        self, e: ft.Event[ft.CupertinoSlidingSegmentedButton] | None = None
    ) -> None:
        self.thumb_color = self._colors[self.selected_index]
        self._toggle_colors()
        if self._actions is not None:
            a = self._actions[self.selected_index]
            if callable(a):
                a()
        self.update()
