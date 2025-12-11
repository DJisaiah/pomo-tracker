import flet as ft
from core.DiscordRPCManager import RPCManager


class PomoUtilities:
	def __init__(self, page):
		self._page = page
		self._dlg = None
		self._RPC = RPCManager()
		self._page.run_task(self._RPC.start_RPC)

	def _get_generic_dialog(self):
		return ft.AlertDialog( 
			title=ft.Text(""),
			content=ft.Text(""), 
			alignment=ft.alignment.center, 
			surface_tint_color=ft.Colors.BLACK)

	def warn_user(self, msg):
		self._dlg = self._get_generic_dialog()
		self._dlg.title = ft.Text("Warning")
		self._dlg.content = ft.Text(msg)
		self._page.open(self._dlg)

	def generic_text_alert(self, title, msg):
		self.generic_alert(title, ft.Text(msg))

	def generic_alert(self, title, msg):
		self._dlg = self._get_generic_dialog()
		self._dlg.title = ft.Text(title)
		self._dlg.content = msg
		self._page.open(self._dlg)

	def text_toast(self, msg):
		self._dlg = self._get_generic_dialog()
		self._dlg.content = ft.Text(
			msg, 
			text_align=ft.TextAlign.CENTER, 
			weight=ft.FontWeight.BOLD
		)
		self._dlg.title=None
		self._dlg.alignment=ft.alignment.center
		self._dlg.bgcolor = ft.Colors.TRANSPARENT
		self._page.open(self._dlg)

	def close_dialog(self):
		self._page.close(self._dlg)

	def add_control(self, control):
		self._page.add(control)

	def play_sound(self, src, autoplay, volume):
		sound = ft.Audio(src=src, autoplay=autoplay,volume=volume)
		self._page.add(sound)

	def get_RPC(self):
		return self._RPC

	def update_page(self):
		self._page.update()
