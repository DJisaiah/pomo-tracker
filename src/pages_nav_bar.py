import flet as ft

def load_nav_bar_and_pages(timer_page, stats_page, feed_page):
    tabs = ft.TabBar(
        tabs=[
            ft.Tab(label="Timer"),
            ft.Tab(label="Stats"),
            ft.Tab(label="Feed"),
            #ft.Tab(label="Settings")
        ],
        tab_alignment=ft.TabAlignment.CENTER,             
        divider_color=ft.Colors.TRANSPARENT,
        indicator_color=ft.Colors.TRANSPARENT,
        overlay_color=ft.Colors.TRANSPARENT,
        label_text_style=ft.TextStyle(
            color=ft.Colors.WHITE_70,
            size=30,
            weight=ft.FontWeight.BOLD
        ),
        unselected_label_text_style=ft.TextStyle(
            color=ft.Colors.GREY_700,
            size=15,
        )
    )

    tab_views = ft.TabBarView(
        expand=True,
        controls=[
            ft.Column(controls=[timer_page.get_page()]),
            ft.Column(controls=[stats_page.get_page()]),
            ft.Column(controls=[feed_page.get_page()])
        ]
    )

    nav_bar = ft.Tabs(
        selected_index=0,
        length=3,
        animation_duration=300,
        content=ft.Column(
            controls=[
                tabs,
                tab_views
            ]
        )
    )
    

    return nav_bar
