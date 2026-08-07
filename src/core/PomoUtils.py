from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Coroutine, cast

import flet as ft
import flet_audio as fta

from core.DiscordRPCManager import DiscordRPCManager
from core.enums import StyleTokens
from core.SubjectUtils import SubjectUtils

if TYPE_CHECKING:
    from core.DBManager import DBManager
    from core.TimerPageUtils import TimerRPCPayload


class PomoUtils:
    def __init__(self, page: ft.Page, db: DBManager, mobile_mode: bool):
        self._page: ft.Page = page
        self._db = db
        self._mobile_mode = mobile_mode
        self._subject_utils = SubjectUtils(self)
        self._dlg = None
        if mobile_mode:
            self._RPC = None
        else:
            self._RPC = DiscordRPCManager()
            self._page.run_task(self._RPC.start_RPC)
        self._finished_audio = fta.Audio(
            src="audio/finished_sound.mp3",
            autoplay=False,
            volume=0.2,
            release_mode=fta.ReleaseMode.STOP,
        )
        self._page.services.append(self._finished_audio)
        self.update_page()

    def get_db(self) -> DBManager:
        return self._db

    def mobile_mode(self) -> bool:
        return self._mobile_mode

    def get_subject_utils(self) -> SubjectUtils:
        return self._subject_utils

    def _get_generic_dialog(self) -> ft.AlertDialog:
        return ft.AlertDialog(
            title=ft.Text(
                "",
                font_family="Space Grotesk",
                text_align=ft.TextAlign.CENTER,
                color=ft.Colors.WHITE,
            ),
            content=ft.Text(
                "",
                text_align=ft.TextAlign.CENTER,
                color=ft.Colors.GREY_400,
                font_family="Space Grotesk-Regular",
            ),
            actions=[
                ft.TextButton(
                    content=ft.Text(
                        "Cool.", color=ft.Colors.BLACK, font_family="Inter-Bold"
                    ),
                    on_click=lambda _: self._page.pop_dialog(),
                    style=ft.ButtonStyle(
                        bgcolor=StyleTokens.POMO_GREEN.value,
                        overlay_color=ft.Colors.GREEN_300,
                    ),
                )
            ],
            bgcolor=StyleTokens.CONTAINER_GREY.value,
            alignment=ft.Alignment.CENTER,
            content_padding=ft.Padding(bottom=30, top=30, left=10, right=10),
            shape=ft.RoundedRectangleBorder(
                radius=10, side=ft.BorderSide(color=ft.Colors.GREY_900, width=1)
            ),
            modal=True,
        )

    def alert_user(self, subject: str, msg: str) -> None:
        self._dlg = self._get_generic_dialog()
        t = cast(ft.Text, self._dlg.title)
        t.value = subject.capitalize()
        c = cast(ft.Text, self._dlg.content)
        c.value = msg.capitalize()

        self._page.show_dialog(self._dlg)

    def simple_alert(self, title: str) -> None:
        self._dlg = self._get_generic_dialog()
        t = cast(ft.Text, self._dlg.title)
        t.value = title.capitalize()
        self._dlg.content = None
        self._page.show_dialog(self._dlg)
        self._page.update()

    def generic_alert(
        self,
        title: str,
        content: ft.Container | ft.Column | ft.Row,
        action: Callable[[ft.Event], None],
    ) -> None:
        def handle_click(e: ft.ControlEvent) -> None:
            action(e)
            self._page.pop_dialog

        self._dlg = self._get_generic_dialog()
        t = cast(ft.Text, self._dlg.title)
        t.value = title.capitalize()
        self._dlg.content = content
        a = cast(ft.TextButton, self._dlg.actions[0])
        a.on_click = action
        self._page.show_dialog(self._dlg)

    def text_toast(self, msg: str) -> None:
        self._dlg = self._get_generic_dialog()
        c = cast(ft.Text, self._dlg.content)
        c.value = msg.capitalize()
        self._page.show_dialog(self._dlg)

    def show_dialog(self, dlg: ft.AlertDialog) -> None:
        self._page.show_dialog(dlg)

    def close_dialog(self) -> None:
        self._page.pop_dialog()

    def add_control(self, control: ft.Control) -> None:
        self._page.add(control)

    def play_finished(self) -> None:
        self.run_task(self._finished_audio.play)

    def get_RPC(
        self, payload: Callable[[], TimerRPCPayload]
    ) -> DiscordRPCManager | None:
        if self._RPC is not None:
            self._RPC.set_payload(payload)
        return self._RPC

    def update_page(self) -> None:
        self._page.update()

    def run_task(
        self, coroutine: Callable[..., Coroutine[Any, Any, Any]], *args: Any
    ) -> None:
        self._page.run_task(coroutine, *args)

    def check_data_integrity(self) -> bool:
        # more integrity checks to come
        valid = self._subject_utils.check_subject_integrity()
        return valid
