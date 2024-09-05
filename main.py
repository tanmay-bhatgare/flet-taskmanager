import flet as ft
from views.login_view import LoginView


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(LoginView(page=page))


ft.app(target=main, assets_dir="./assets")
