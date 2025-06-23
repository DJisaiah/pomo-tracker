import flet as ft

def main(page: ft.Page):
    page.title = "Pomo-Tracker"
    timer_text = ft.Text("25:00", size=150)
    page.add(
        ft.Row(controls=[timer_text], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(controls=[
            ft.IconButton(
                icon=ft.Icons.PLAY_CIRCLE,
                icon_size=90,
                tooltip="Start the timer"
            ),
            ft.IconButton(
                icon=ft.Icons.STOP_CIRCLE,
                icon_size=90,
                tooltip="Stop the timer"
            ),
            ft.CircleAvatar(
                content=ft.Text("Custom Timer", text_align=ft.TextAlign.CENTER),
                radius=40,
                tooltip="Set a custom timer"
            ),
            ft.CircleAvatar(
                content=ft.Text("Stopwatch Mode", text_align=ft.TextAlign.CENTER),
                radius=40,
                tooltip="Act as a stopwatch and stop when the user wants"
            ),
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

ft.app(main)