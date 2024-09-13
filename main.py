import warnings
import flet as ft

# from utils
from utils.view_handler import view_handler
from constants.constants import Routes

warnings.filterwarnings("ignore")


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
        except Exception:
            view_handler(page)[Routes.error_page]
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

    page.go("/")


ft.app(target=main, assets_dir="./assets")
