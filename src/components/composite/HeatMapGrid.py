from __future__ import annotations

import calendar
from datetime import datetime
from typing import TYPE_CHECKING

import flet as ft

from components.base.HeatMapSquare import HeatMapSquare

if TYPE_CHECKING:
    from core.DBManager import DBManager


class HeatMapGrid(ft.Container):
    def __init__(self, db: DBManager):
        super().__init__(
            height=350,
            width=530,
            padding=10,
            bgcolor=ft.Colors.BLACK_87,
            border_radius=ft.BorderRadius.all(6),
            border=ft.Border.all(width=2, color=ft.Colors.GREY_900),
        )
        self._db: DBManager = db

        # controls
        self._grid_rows: ft.Row = self._create_heatmap_squares()

        self.content = ft.Column(
            controls=[
                ft.Text(
                    "365 DAYS",
                    size=14,
                    text_align=ft.TextAlign.LEFT,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_700,
                ),
                self._grid_rows,
            ]
        )

    def _create_heatmap_squares(self) -> ft.Row:
        month_name_col = ft.Column(
            controls=[ft.Container(height=3)],
            spacing=2,
            alignment=ft.MainAxisAlignment.START,
        )

        all_month_blocks = ft.Column(controls=[ft.Container()])
        for month in range(1, 13):
            year = datetime.now().year
            month_days = calendar.monthrange(year, month)[1]
            month_name = calendar.month_abbr[month]
            month_name_col.controls.append(
                ft.Text(
                    f"{month_name}",
                    size=15,
                    color=ft.Colors.GREY_500,
                    weight=ft.FontWeight.W_300,
                )
            )
            month_blocks = ft.Row(spacing=2)
            for day in range(1, month_days + 1):
                count = self._db.get_day_session_count(year, month, day)
                month_blocks.controls.append(HeatMapSquare(count, width=13, height=13))
            all_month_blocks.controls.append(month_blocks)

        months_grid = ft.Row(
            controls=[month_name_col, all_month_blocks],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        return months_grid
