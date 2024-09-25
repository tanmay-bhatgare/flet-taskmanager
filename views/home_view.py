# from typing import Any, Dict, List
import flet as ft
from icecream import ic

from widgets.widgets import TaskCard
from constants.constants import Pallet, Urls
from controllers.controllers import TaskController
# from utils.jwt_token_encoder import decrypt_jwt
# from utils.session_storage_setter import async_get_session_value

ic.configureOutput(prefix="Debug | ", includeContext=True)


temp_tasks: list[dict] = [
    {
        "title": "string",
        "description": "string string string string string string string string string string string string string",
        "is_private": True,
        "id": 0,
        "owner_id": 0,
        "created_at": "2024-09-20T12:15:48.251Z",
        "is_completed": True,
        "due_date": "2024-09-20T12:15:48.251Z",
        "completed_at": "2024-09-20T12:15:48.251Z",
    },
    {
        "title": "string",
        "description": "string",
        "is_private": True,
        "id": 0,
        "owner_id": 0,
        "created_at": "2024-09-20T12:15:48.251Z",
        "is_completed": True,
        "due_date": "2024-09-20T12:15:48.251Z",
        "completed_at": "2024-09-20T12:15:48.251Z",
    },
    {
        "title": "string",
        "description": "string",
        "is_private": True,
        "id": 0,
        "owner_id": 0,
        "created_at": "2024-09-20T12:15:48.251Z",
        "is_completed": True,
        "due_date": "2024-09-20T12:15:48.251Z",
        "completed_at": "2024-09-20T12:15:48.251Z",
    },
    {
        "title": "string",
        "description": "string",
        "is_private": True,
        "id": 0,
        "owner_id": 0,
        "created_at": "2024-09-20T12:15:48.251Z",
        "is_completed": True,
        "due_date": "2024-09-20T12:15:48.251Z",
        "completed_at": "2024-09-20T12:15:48.251Z",
    },
    {
        "title": "string",
        "description": "string",
        "is_private": True,
        "id": 0,
        "owner_id": 0,
        "created_at": "2024-09-20T12:15:48.251Z",
        "is_completed": True,
        "due_date": "2024-09-20T12:15:48.251Z",
        "completed_at": "2024-09-20T12:15:48.251Z",
    },
]


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
        self.controller = TaskController(
            jwt_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0LCJleHAiOjE3MjcyNzU0NDh9.CfZy--i5l710k5hv1OFg11nUQXC3a5vKRbgbIOmcsc4"
        )
        tasks = await self.controller.get_tasks(url=Urls.get_tasks_url)
        self.tasks = tasks
        self.update_list_view()

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
        self.page.run_task(self.fetch_tasks)  # Re-fetch tasks on button click

    def did_mount(self):
        ic("Control Mounted")
        future = self.page.run_task(self.fetch_tasks)
        future.add_done_callback(lambda f: ic(f.result()))

    def build(self) -> ft.Control:
        self.__build_content = ft.ListView(
            controls=[],  # Initialize with empty controls
            spacing=10,
        )
        # Return the layout with the button and the ListView
        return self.__build_content
