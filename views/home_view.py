# from typing import Any, Dict, List
from typing import Any, Dict
import flet as ft
from icecream import ic

from widgets.widgets import TaskCard
from constants.constants import Pallet, Urls, SessionKey
from controllers.controllers import TaskController
from utils.jwt_token_encoder import decrypt_jwt
from utils.session_storage_setter import async_get_session_value

ic.configureOutput(prefix="Debug | ", includeContext=True)


class HomeView(ft.UserControl):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.page: ft.Page = page
        self.controller: TaskController | None = None
        self.tasks: list[dict] = []
        self.page.theme = ft.Theme(
            scrollbar_theme=ft.ScrollbarTheme(
                track_color={
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                    ft.ControlState.HOVERED: ft.colors.TRANSPARENT,
                },
                track_visibility=False,
                thumb_visibility=False,
                thumb_color={
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                    ft.ControlState.HOVERED: ft.colors.TRANSPARENT,
                },
            )
        )

    async def fetch_tasks(self):
        ic("Fetching Tasks")
        token: str | None = await async_get_session_value(
            page=self.page, key=SessionKey.access_token
        )
        self.controller: TaskController = TaskController(jwt_token=decrypt_jwt(token))
        tasks: Dict[str, Any] | None = await self.controller.get_tasks(
            url=Urls.get_tasks_url
        )
        self.tasks: Dict[str, Any] | None = tasks
        if self.tasks:
            self.update_list_view()
        else:
            ic("No Tasks Found")
            self.__build_content.controls = [
                ft.Text("No Tasks Found", color="red", size=20)
            ]
            self.__build_content.update()
            # self.page.update()

    def update_list_view(self):
        self.__build_content.controls = [
            TaskCard(
                width=self.page.width,
                background_color=Pallet.card_bg_color,
                update_function=lambda _: print("Update"),
                delete_function=lambda _: print("Delete"),
                **task,
            )
            for task in self.tasks
        ]
        self.__build_content.update()

    def refresh_tasks(self):
        ic("Refreshing Tasks")
        self.page.run_task(self.fetch_tasks)

    def did_mount(self):
        ic("Control Mounted")
        future = self.page.run_task(self.fetch_tasks)
        future.add_done_callback(lambda f: ic(f.result()))

    def build(self) -> ft.Control:
        self.__build_content = ft.ListView(
            controls=[],
            spacing=10,
        )
        # Return the layout with the button and the ListView
        return self.__build_content
