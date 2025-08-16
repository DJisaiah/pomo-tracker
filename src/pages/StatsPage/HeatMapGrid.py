import flet as ft

class HeatMapGrid:
    def __init__(self):
        self._heatmap_grid = ft.GridView(
            max_extent=17,
            spacing=3,
            run_spacing=3,
            padding=12,
            child_aspect_ratio=1.0
        )

        self._heatmap_container = ft.Container(
            content=self._heatmap_grid,
            bgcolor=ft.Colors.GREY_900,
            border_radius=ft.border_radius.all(6)
        )

        self._create_heatmap_squares()

    def _create_heatmap_squares(self):

        def hover_text(e):
            e.control.content = ft.Text(1, text_align=ft.TextAlign.CENTER) if e.data == "true" else None
            e.control.update()

        for _ in range(371):
            self._heatmap_grid.controls.append(
                ft.Container(
                    bgcolor=ft.Colors.GREEN_800,
                    border_radius=ft.border_radius.all(3),
                    height=10,
                    width=10,
                    on_hover=hover_text
                )
            )
    
    def get_heatmap(self):
        return self._heatmap_container
