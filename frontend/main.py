# TODO: frontend\.venv\Lib\site-packages\flet_core\page.py(1360)

import warnings
import flet as ft
from icecream import ic
import asyncio

# from utils
from utils.view_handler import view_handler
from constants.constants import Routes, SessionKey
from utils.session_storage_setter import async_get_session_value
from utils.auto_logout import check_session_timeout


warnings.filterwarnings("ignore")
ic.configureOutput(prefix="Debug | ", includeContext=True)


async def main(page: ft.Page):
    asyncio.create_task(
        check_session_timeout(
            page=page,
            login_timestamp_key=SessionKey.login_timestamp,
            is_logged_in_key=SessionKey.is_logged_in,
            session_timeout_min=60,
        )
    )
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "Task Manager"
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_color={ft.ControlState.DEFAULT: ft.colors.RED},
            thumb_color={ft.ControlState.DEFAULT: ft.colors.PURPLE},
            track_visibility=False,
            thumb_visibility=False,
        )
    )
    __is_logged_in = await async_get_session_value(
        page=page, key=SessionKey.is_logged_in
    )

    history = []

    def route_change(event: ft.RouteChangeEvent):
        route = event.route
        if page.views:
            history.append(page.views[-1].route)

        page.views.clear()
        try:
            if __is_logged_in and (
                route == Routes.login_route or route == Routes.sign_up_route
            ):
                page.views.append(
                    view_handler(page)[Routes.home_route],
                )
            else:
                page.views.append(
                    view_handler(page)[route],
                )
        except Exception as e:
            page.views.append(view_handler(page)[Routes.login_route])
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

    if __is_logged_in:
        page.go(Routes.home_route)
    else:
        page.go(Routes.login_route)


ft.app(target=main, assets_dir="assets")
