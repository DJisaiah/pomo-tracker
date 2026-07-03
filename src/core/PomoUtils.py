from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Callable

import flet as ft
import flet_audio as fta

from core.DiscordRPCManager import DiscordRPCManager

if TYPE_CHECKING:
    from core.DBManager import DBManager


class PomoUtils:
    def __init__(self, page: ft.Page, db: DBManager):
        self._page: ft.Page = page
        self._db = db
        self._dlg = None
        self._RPC = DiscordRPCManager()
        # for now
        self._page.run_task(self._RPC.start_RPC)
        self._finished_audio = fta.Audio(
            src="audio/finished_sound.mp3",
            autoplay=False,
            volume=0.2,
            release_mode=fta.ReleaseMode.STOP,
        )
        self._page.services.append(self._finished_audio)

    def get_db(self) -> DBManager:
        return self._db

    def _get_generic_dialog(self) -> ft.AlertDialog:
        return ft.AlertDialog(
            bgcolor=ft.Colors.BLACK,
            title=ft.Text(""),
            content=ft.Text(""),
            alignment=ft.Alignment.CENTER,
            shape=ft.RoundedRectangleBorder(
                radius=10, side=ft.BorderSide(color=ft.Colors.GREY_700, width=2)
            ),
            actions=[
                ft.TextButton(
                    content=ft.Text("Cool.", color=ft.Colors.GREEN_700),
                    on_click=lambda e: self._page.pop_dialog(),
                )
            ],
        )

    def alert_user(self, subject: str, msg: str) -> None:
        self._dlg = self._get_generic_dialog()
        self._dlg.title = ft.Text(
            subject, text_align=ft.TextAlign.CENTER, color=ft.Colors.WHITE_70
        )
        self._dlg.content = ft.Text(
            msg, text_align=ft.TextAlign.CENTER, color=ft.Colors.WHITE_70
        )
        self._page.show_dialog(self._dlg)

    def simple_alert(self, title: str) -> None:
        self._dlg = self._get_generic_dialog()
        self._dlg.title = ft.Text(
            title,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE_70,
        )
        self._dlg.content = None
        self._page.show_dialog(self._dlg)
        self._page.update()

    def generic_alert(
        self,
        title: str,
        content: ft.Container | ft.Column | ft.Row,
        action: Callable[[ft.ControlEvent], None],
    ) -> None:
        def handle_click(e: ft.ControlEvent) -> None:
            action(e)
            self._page.pop_dialog

        self._dlg = self._get_generic_dialog()
        self._dlg.title = ft.Text(
            title, text_align=ft.TextAlign.CENTER, color=ft.Colors.WHITE_70
        )
        self._dlg.content = content
        self._dlg.actions = [  # type: ignore
            ft.TextButton(
                content=ft.Text("Cool.", color=ft.Colors.GREEN_700),
                on_click=handle_click,  # type: ignore
            )
        ]
        self._page.show_dialog(self._dlg)

    def text_toast(self, msg: str) -> None:
        self._dlg = self._get_generic_dialog()
        self._dlg.content = ft.Text(
            msg,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE_70,
        )
        self._dlg.title = None
        self._dlg.alignment = ft.Alignment.CENTER
        self._dlg.bgcolor = ft.Colors.TRANSPARENT
        self._page.show_dialog(self._dlg)

    def show_dialog(self, dlg: ft.AlertDialog) -> None:
        self._page.show_dialog(dlg)

    def close_dialog(self) -> None:
        self._page.pop_dialog()

    def add_control(self, control: ft.Control) -> None:
        self._page.add(control)

    def play_finished(self) -> None:
        asyncio.create_task(self._finished_audio.play())

    def get_RPC(self) -> DiscordRPCManager:
        return self._RPC

    def update_page(self) -> None:
        self._page.update()
