import flet as ft
from constants.constants import Routes
from views.views import HomeView, LoginView


def view_handler(page: ft.Page):
    return {
        f"{Routes.home_route}": ft.View(
            appbar=ft.AppBar(
                title=ft.Text(
                    "Welcome to the Homepage", size=20, color=ft.colors.WHITE
                ),
                bgcolor=ft.colors.BLUE_700,
            ),
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            route=Routes.home_route,
            controls=[HomeView(page=page)],
        ),
        f"{Routes.login_route}": ft.View(
            appbar=ft.AppBar(
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK
                    if page.platform
                    in [
                        ft.PagePlatform.WINDOWS,
                        ft.PagePlatform.LINUX,
                        ft.PagePlatform.ANDROID,
                    ]
                    else ft.icons.ARROW_BACK_IOS_NEW,
                    on_click=lambda _: page.go("/"),
                ),
                automatically_imply_leading=True,
                title=ft.Text("Login", size=20, color=ft.colors.WHITE),
                bgcolor=ft.colors.SURFACE_VARIANT,
            ),
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            route=Routes.login_route,
            controls=[LoginView(page=page)],
        ),
    }
