import flet as ft
import calendar
from datetime import datetime

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

        def hover_text(e):
            e.control.content = ft.Text(count, text_align=ft.TextAlign.CENTER, color=ft.Colors.BLACK) if e.data == "true" else None
            e.control.update()

        def get_colour():
            # fetch pomo count from db TODO
            
            if count == 0:
                colour = ft.Colors.GREY_300
            elif count >=1 and count <=3:
                colour = ft.Colors.GREEN_300
            elif count > 3 and count < 5:
                colour = ft.Colors.GREEN_500
            elif count >= 5 and count < 8:
                colour = ft.Colors.GREEN_700
            else:
                colour = ft.Colors.GREEN_900

            return colour


        month_name_col = ft.Column(controls=[ft.Container(height=3)], spacing=2, alignment=ft.MainAxisAlignment.START)
        all_month_blocks = ft.Column(controls=[ft.Container()])
        for month in range(1, 13):
            year = datetime.now().year
            month_days = calendar.monthrange(year, month)[1]
            month_name = calendar.month_abbr[month]
            month_name_col.controls.append(
                ft.Text(f"{month_name}", size=15)
            )
            
            month_blocks = ft.Row(
                spacing=2
            )

            for day in range(1, month_days + 1):
                count = self._db.get_day_session_count(year, month, day)
                month_blocks.controls.append(
                    ft.Container(
                        bgcolor=get_colour(),
                        border_radius=ft.border_radius.all(3),
                        width=13,
                        height=13,
                        on_hover=hover_text
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
