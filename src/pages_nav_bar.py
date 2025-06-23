import flet as ft

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