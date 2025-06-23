import asyncio
import flet as ft

def main(page: ft.Page):
    page.title = "Pomo-Tracker"
    pomodoro = 10
    timer_text = ft.Row(controls=[ft.Text("25:00", size=150)],
                        alignment=ft.MainAxisAlignment.CENTER)
    timer_running = False

    async def start_timer(e):
        nonlocal timer_running
        if timer_running:
            return
        else:
            timer_running = True

        start_button = buttons.controls[0]
        current_time = pomodoro
        timer = timer_text.controls[0]
        start_button.disabled = True
        while current_time >= 0:
            minutes = current_time // 60
            seconds = current_time % 60
            timer.value = f"{minutes:02d}:{seconds:02d}"
            page.update()
            await asyncio.sleep(1)
            current_time -= 1
        timer.value = "Timer Finished!"

    buttons = ft.Row(controls=[
        ft.IconButton(
            icon=ft.Icons.PLAY_CIRCLE,
            icon_size=90,
            tooltip="Start the timer",
            on_click=start_timer,
            disabled_color = ft.Colors.GREY
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

    nav_bar = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Timer",
                content=ft.Column(controls=[timer_text, buttons])
            ),
            ft.Tab(
                text="Stats",
                content=ft.Text("Stats Section", size=100)
            ),
            ft.Tab(
                text="Rankings",
                content=ft.Text("Rankings Section", size=100)
            ),
            ft.Tab(
                text="Settings",
                content=ft.Text("Settings Section", size=100)
            )
        ],
        tab_alignment=ft.TabAlignment.CENTER
    )

    page.add(
        nav_bar
    )

ft.app(main)
