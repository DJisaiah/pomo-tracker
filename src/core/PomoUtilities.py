from __future__ import annotations
from typing import TYPE_CHECKING
import flet as ft
from core.DiscordRPCManager import RPCManager

if TYPE_CHECKING:
    from database.local_db import LocalDB


class PomoUtilities:
    def __init__(self, page: ft.Page, db: LocalDB):
        self._page: ft.Page = page
        self._db: LocalDB = db
        self._dlg = None
        self._RPC: RPCManager = RPCManager()
        self._page.run_task(self._RPC.start_RPC)

    def get_db(self) -> LocalDB:
        return self._db

    def _get_generic_dialog(self) -> ft.AlertDialog:
        return ft.AlertDialog( 
			title=ft.Text(""),
			content=ft.Text(""), 
			alignment=ft.alignment.center, 
			surface_tint_color=ft.Colors.BLACK
        )

    def warn_user(self, msg: str) -> None:
        self._dlg = self._get_generic_dialog()
        self._dlg.title = ft.Text("Warning")
        self._dlg.content = ft.Text(msg)
        self._page.open(self._dlg)

    def generic_text_alert(self, title: str, msg: str) -> None:
        self.generic_alert(title, ft.Text(msg))

    def generic_alert(self, title: str, msg: str) -> None:
        self._dlg = self._get_generic_dialog()
        self._dlg.title = ft.Text(title)
        self._dlg.content = msg
        self._page.open(self._dlg)

    def text_toast(self, msg: str) -> None:
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

    def close_dialog(self) -> None:
        self._page.close(self._dlg)

    def add_control(self, control) -> None:
        self._page.add(control)

    def play_sound(self, src: str, autoplay: bool, volume: float) -> None:
        sound = ft.Audio(src=src, autoplay=autoplay,volume=volume)
        self._page.add(sound)

    def get_RPC(self) -> None:
        return self._RPC

    def update_page(self) -> None:
        self._page.update()
