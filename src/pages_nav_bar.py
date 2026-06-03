import flet as ft

def load_nav_bar_and_pages(timer_page, stats_page):
    tabs = ft.TabBar(
        tabs=[
            ft.Tab(label="Timer"),
            ft.Tab(label="Stats"),
            #ft.Tab(label="Feed"),
            #ft.Tab(label="Settings")
        ],
        tab_alignment=ft.TabAlignment.CENTER,             
        divider_color=ft.Colors.TRANSPARENT,
        indicator_color=ft.Colors.GREEN_200,
        label_color=ft.Colors.GREEN_200,
        overlay_color=ft.Colors.TRANSPARENT
    )

    tab_views = ft.TabBarView(
        expand=True,
        controls=[
            ft.Column(controls=[timer_page.get_page()]),
            ft.Column(controls=[stats_page.get_page()])
            #ft.Text("", size=100),
            #ft.Text("", size=100)
        ]
    )

    nav_bar = ft.Tabs(
        selected_index=0,
        length=2,
        animation_duration=300,
        content=ft.Column(
            controls=[
                tabs,
                tab_views
            ]
        )
    )
    

    return nav_bar
