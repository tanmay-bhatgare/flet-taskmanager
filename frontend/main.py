import warnings
import flet as ft
from icecream import ic


# from utils
from utils.view_handler import view_handler
from constants.constants import Routes, SessionKey
from utils.session_storage_setter import async_get_session_value

warnings.filterwarnings("ignore")
ic.configureOutput(prefix="Debug | ", includeContext=True)


async def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    history = []

    def route_change(event: ft.RouteChangeEvent):
        route = event.route
        if page.views:
            history.append(page.views[-1].route)

        page.views.clear()
        try:
            page.views.append(
                view_handler(page)[route],
            )
        except Exception as e:
            ic(e)
        page.update()

    def view_pop(view):
        if len(page.views) > 1:
            history.pop()

            previous_route = history.pop() if history else "/"
            page.go(previous_route)
        else:
            page.go("/")

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    __is_logged_in = await async_get_session_value(
        page=page, key=SessionKey.is_logged_in
    )

    if __is_logged_in:
        page.go(Routes.home_route)
    else:
        page.go(Routes.login_route)


ft.app(target=main, assets_dir="./assets")
