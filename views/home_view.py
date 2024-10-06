from typing import Any, Dict
import flet as ft
from icecream import ic

from widgets.widgets import TaskCard, UpdateTaskCard
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
        self.__delete_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirm Delete"),
            content=ft.Text("Can't Undone this!"),
            actions=[
                ft.TextButton(
                    "Yes",
                    on_click=self.__handle_delete_yes,
                    style=ft.ButtonStyle(
                        bgcolor=Pallet.transparent,
                        shape=ft.RoundedRectangleBorder(5),
                        padding=ft.padding.symmetric(vertical=10, horizontal=14),
                    ),
                ),
                ft.TextButton(
                    "No",
                    on_click=self.__handle_delete_no,
                    style=ft.ButtonStyle(
                        bgcolor=Pallet.transparent,
                        shape=ft.RoundedRectangleBorder(5),
                        padding=ft.padding.symmetric(vertical=10, horizontal=14),
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            data=None,
        )
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

    async def __handle_delete_yes(self, e):
        task_id = self.__delete_dialog.data
        response = await self.controller.delete_task(
            url=f"{Urls.delete_task_url}/{task_id}"
        )
        if response:
            self.refresh_tasks()
        self.page.close(self.__delete_dialog)

    def __handle_delete_no(self, e):
        self.page.close(self.__delete_dialog)

    def handle_delete(self, task_id: int):
        self.__delete_dialog.data = task_id
        self.page.open(self.__delete_dialog)

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

    def update_list_view(self):
        self.__build_content.controls = [
            TaskCard(
                width=self.page.width,
                background_color=Pallet.card_bg_color,
                update_function=lambda _, task_id=task["id"]: print(
                    f"Update {task_id}"
                ),
                delete_function=lambda _, task_id=task["id"]: self.handle_delete(
                    task_id=task_id
                ),
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

    def open_dlg(self):
        self.page.open(self.__delete_dialog)

    def trial_func(self, e):
        
        update_task_card = UpdateTaskCard(
            width=self.page.width * 0.98,
            title="Centered Task Card",
            background_color=Pallet.card_bg_color,
        )

        centered_container = ft.Container(
            content=update_task_card,
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=ft.colors.with_opacity(0.7, ft.colors.BLACK),
        )
        if self.page.overlay:
            self.page.overlay.pop()
        self.page.overlay.append(centered_container)

        self.page.update()

    def build(self) -> ft.Control:
        self.__build_content = ft.ListView(
            controls=[],
            spacing=10,
        )

        return self.__build_content
