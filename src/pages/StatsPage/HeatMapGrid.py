import flet as ft
import calendar
from datetime import datetime
from .HeatMapSquare import HeatMapSquare


class HeatMapGrid:
    def __init__(self, db):
        self._db = db
        grid_rows = self._create_heatmap_squares()
        self._heatmap_container = ft.Container(
            content=ft.Column(controls=[
                ft.Text("365 Days", size=20, text_align=ft.TextAlign.LEFT, weight=ft.FontWeight.BOLD),
                grid_rows
            ]),
            bgcolor=ft.Colors.GREY_900,
            border_radius=ft.border_radius.all(6),
            height=350,
            width=530,
            padding=10
        )

    def _create_heatmap_squares(self):
        month_name_col = ft.Column(controls=[ft.Container(height=3)], spacing=2, alignment=ft.MainAxisAlignment.START)
        all_month_blocks = ft.Column(controls=[ft.Container()])
        for month in range(1, 13):
            year = datetime.now().year
            if month < 10:
                padded_month = f"0{month}"
            else:
                padded_month = month
            month_days = calendar.monthrange(year, month)[1]
            month_name = calendar.month_abbr[month]
            month_name_col.controls.append(
                ft.Text(f"{month_name}", size=15)
            )
            month_blocks = ft.Row(
                spacing=2
            )
            for day in range(1, month_days + 1):
                if day < 10:
                    padded_day = f"0{day}"
                else:
                    padded_day = day
                count = self._db.get_day_session_count(year, padded_month, padded_day)
                month_blocks.controls.append(
                    HeatMapSquare(
                        count,
                        width=13,
                        height=13
                        )
                    )
            all_month_blocks.controls.append(month_blocks)

        months_grid = ft.Row(
            controls=[month_name_col, all_month_blocks],
            alignment=ft.MainAxisAlignment.CENTER
            )
        return months_grid
    
    def get_heatmap(self):
        return self._heatmap_container
