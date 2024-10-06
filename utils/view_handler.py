import flet as ft
from constants.constants import Routes
from views.views import HomeView, LoginView, SignUpView


def view_handler(page: ft.Page):
    home_view = HomeView(page=page)
    return {
        # ? Home View
        f"{Routes.home_route}": ft.View(
            scroll="always",
            route=Routes.home_route,
            appbar=ft.AppBar(
                leading=ft.Icon(name=ft.icons.TASK_ALT_SHARP),
                leading_width=30,
                title=ft.Text("Task Manager", size=20, color=ft.colors.WHITE),
                bgcolor="#2b2d42",
                actions=[
                    ft.IconButton(
                        icon=ft.icons.REFRESH,
                        on_click=lambda _: home_view.refresh_tasks(),
                    ),
                ],
            ),
            floating_action_button=ft.FloatingActionButton(
                icon=ft.icons.ADD, on_click=home_view.trial_func, bgcolor="#60a5fa"
            ),
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[home_view],
        ),
        # ? Sign Up View
        f"{Routes.sign_up_route}": ft.View(
            route=Routes.sign_up_route,
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
                    on_click=lambda _: page.go(Routes.login_route),
                ),
                title=ft.Text("Sign Up", size=20, color=ft.colors.WHITE),
                automatically_imply_leading=True,
                bgcolor="#2b2d42",
            ),
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[SignUpView(page=page)],
        ),
        # ? Sign In View
        f"{Routes.login_route}": ft.View(
            route=Routes.login_route,
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
                    on_click=lambda _: page.go(Routes.sign_up_route),
                ),
                automatically_imply_leading=True,
                title=ft.Text("Login", size=20, color=ft.colors.WHITE),
                bgcolor="#2b2d42",
            ),
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[LoginView(page=page)],
        ),
    }
