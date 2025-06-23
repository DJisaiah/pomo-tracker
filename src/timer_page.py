import flet as ft
import 

pomodoro = 10
timer_running = False

timer_text = ft.Row(controls=[ft.Text("25:00", size=150)],
                        alignment=ft.MainAxisAlignment.CENTER)

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
