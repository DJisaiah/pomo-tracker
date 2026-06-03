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
        #self.close_dialog()
        return ft.AlertDialog( 
			title=ft.Text(""),
			content=ft.Text(""), 
			alignment=ft.Alignment.CENTER, 
            shape=ft.RoundedRectangleBorder(
                radius=10
            ),
            actions = [ft.TextButton(
                content=ft.Text("Cool.", color=ft.Colors.GREEN_700),
                on_click= lambda e: self._page.pop_dialog()
                )
            ]
        )

    def alert_user(self, subject: str, msg: str) -> None:
        self._dlg = self._get_generic_dialog()
        self._dlg.title = ft.Text(subject, text_align=ft.TextAlign.CENTER)
        self._dlg.content = ft.Text(msg, text_align=ft.TextAlign.CENTER)
        self._page.show_dialog(self._dlg)

    def simple_alert(self, title: str) -> None:
        self._dlg = self._get_generic_dialog()
        self._dlg.title = ft.Text(title, text_align=ft.TextAlign.CENTER)
        self._page.show_dialog(self._dlg)
        self._page.update()

    def generic_alert(self, 
        title: str,
        content: ft.Container | ft.Column | ft.Row,
        action: Callable[[ft.ControlEvent], None]) -> None:
        self._dlg = self._get_generic_dialog()
        self._dlg.title = ft.Text(title, text_align=ft.TextAlign.CENTER)
        self._dlg.content = content
        self._dlg.actions = [ft.TextButton(
            content=ft.Text("Cool.", color=ft.Colors.GREEN_700),
            on_click= lambda e: (self._page.pop_dialog(), action())
        )
        ]
        self._page.show_dialog(self._dlg)

    def text_toast(self, msg: str) -> None:
        self._dlg = self._get_generic_dialog()
        self._dlg.content = ft.Text(
            msg, 
            text_align=ft.TextAlign.CENTER, 
            weight=ft.FontWeight.BOLD
        )
        self._dlg.title=None
        self._dlg.alignment=ft.Alignment.CENTER
        self._dlg.bgcolor = ft.Colors.TRANSPARENT
        self._page.show_dialog(self._dlg)

    def close_dialog(self) -> None:
        self._page.pop_dialog()

    def add_control(self, control) -> None:
        self._page.add(control)

    def play_sound(self, src: str, autoplay: bool, volume: float) -> None:
        sound = ft.Audio(src=src, autoplay=autoplay,volume=volume)
        self._page.add(sound)

    def get_RPC(self) -> None:
        return self._RPC

    def update_page(self) -> None:
        self._page.update()
