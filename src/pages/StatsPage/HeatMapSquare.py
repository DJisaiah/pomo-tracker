import flet as ft


class HeatMapSquare(ft.Container):
	def __init__(self, count, width, height):
		self._count = count
		super().__init__(
			bgcolor=self._get_colour(),
			border_radius=ft.border_radius.all(3),
			width=width,
			height=height,
			on_hover=self._hover_text,
			alignment=ft.alignment.center,
			)

	def _hover_text(self, e):
	    e.control.content = ft.Text(self._count, text_align=ft.TextAlign.CENTER, 
	    	color=ft.Colors.WHITE, size=10, 
	    	weight=ft.FontWeight.BOLD) if e.data == "true" else None
	    e.control.update()


	def _get_colour(self):
	    # fetch pomo count from db TODO
	    
	    if self._count == 0:
	        colour = ft.Colors.GREY_700
	    elif self._count >=1 and self._count <=3:
	        colour = ft.Colors.GREEN_300
	    elif self._count > 3 and self._count < 5:
	        colour = ft.Colors.GREEN_500
	    elif self._count >= 5 and self._count < 8:
	        colour = ft.Colors.GREEN_700
	    else:
	        colour = ft.Colors.GREEN_900

	    return colour