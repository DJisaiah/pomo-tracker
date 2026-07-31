from __future__ import annotations

import calendar
from datetime import datetime
from typing import TYPE_CHECKING, cast

import flet as ft

from components.base.HeatMapSquare import HeatMapSquare

if TYPE_CHECKING:
    from core.DBManager import DBManager


class HeatMapGrid(ft.Container):
    def __init__(self, db: DBManager, mobile: bool):
        super().__init__(padding=10)
        self._db: DBManager = db
        self._mobile = mobile

        self._grid_rows: ft.Row = self._create_heatmap_squares()

        self.content = ft.Column(
            controls=[
                self._grid_rows,
            ]
        )

    def _create_heatmap_squares(self) -> ft.Row:
        month_name_col = ft.Column(
            controls=[ft.Container(height=3)],
            spacing=2,
            alignment=ft.MainAxisAlignment.START,
        )

        if self._mobile:
            block_height = 8
            block_width = 8
            text_size = 12
            text_width = 25
            rounding = 2
        else:
            block_height = 13
            block_width = 13
            text_size = 15
            text_width = 40
            rounding = 4

        self._all_month_blocks = ft.Column(controls=[ft.Container()])
        for month in range(1, 13):
            year = datetime.now().year
            month_days = calendar.monthrange(year, month)[1]
            month_name = calendar.month_abbr[month]
            month_name_col.controls.append(
                mn := ft.Text(
                    f"{month_name}",
                    size=text_size,
                    color=ft.Colors.GREY_500,
                    weight=ft.FontWeight.W_300,
                    width=text_width,
                )
            )
            month_blocks = ft.Row(spacing=2)
            month_blocks.controls.append(mn)
            for day in range(1, month_days + 1):
                count = self._db.get_day_session_count(year, month, day)
                month_blocks.controls.append(
                    HeatMapSquare(
                        count=count,
                        width=block_width,
                        height=block_height,
                        rounding=rounding,
                    )
                )
            self._all_month_blocks.controls.append(month_blocks)

        months_grid = ft.Row(
            controls=[self._all_month_blocks],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        return months_grid

    def soft_refresh(self, count: int) -> None:
        today = datetime.now()
        month_index = today.month
        day_index = today.day
        month_row = cast(ft.Row, self._all_month_blocks.controls[month_index])
        day_square = cast(HeatMapSquare, month_row.controls[day_index])
        day_square.increment(count)

    def hard_refresh(self) -> None:
        self._grid_rows = self._create_heatmap_squares()
        cast(ft.Column, self.content).controls = [self._grid_rows]
