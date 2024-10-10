from typing import Any, Dict
import flet as ft
from icecream import ic

from widgets.widgets import TaskCard, PopUpTaskCard
from constants.constants import Pallet, Urls, SessionKey
from controllers.controllers import TaskController
from utils.jwt_token_encoder import decrypt_jwt
from utils.session_storage_setter import async_get_session_value
from utils.date_converter import ISO8601_to_std
from models.models import TaskResponseModel, UpdateTaskModel, CreateTaskModel


ic.configureOutput(prefix="Debug | ", includeContext=True)


class HomeView(ft.UserControl):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.page: ft.Page = page
        self.controller: TaskController | None = None
        self.tasks: list[dict] = []
        self._create_task_card = PopUpTaskCard(
            type="create",
            width=self.page.width * 0.98,
            background_color=Pallet.card_bg_color,
            submit_function=self.create_task,
        )
        self._update_task_card = PopUpTaskCard(
            type="update",
            width=self.page.width * 0.98,
            background_color=Pallet.card_bg_color,
            submit_function=self.update_task,
        )

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

    def open_delete_dlg(self, task_id: int):
        self.__delete_dialog.data = task_id
        self.page.open(self.__delete_dialog)

    async def create_task(self, e):
        ic("Creating Task")
        task_data: CreateTaskModel = self._create_task_card.return_data()
        print(task_data)

        if task_data.title and task_data.description and task_data.due_date:
            response = await self.controller.create_task(
                url=Urls.create_task_url, task_data=task_data
            )

            if response:
                self.refresh_tasks()
            self.page.overlay.remove(self._create_task_centered_container)
            self.page.update()
        else:
            ic("All Fields Are Required!")
        self._create_task_card._title_textfield.value = ""
        self._create_task_card._description_textfield.value = ""
        self.page.update()

    async def update_task(self, e):
        ic("Updating Task")
        task_id: int = self._update_task_card.data
        task_data: UpdateTaskModel = self._update_task_card.return_data()
        print(task_data)

        if task_data.title and task_data.description and task_data.due_date:
            response = await self.controller.update_task(
                url=f"{Urls.update_task_url}/{task_id}", task_data=task_data
            )
            if response:
                self.refresh_tasks()
            self.page.overlay.remove(self._update_task_centered_container)
            self.page.update()
        else:
            ic("All Field Are Required!")
        self.page.update()

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
                update_function=lambda _,
                task_model=TaskResponseModel(**task): self.show_update_task_popup(
                    task_model=task_model
                ),
                delete_function=lambda _, task_id=task["id"]: self.open_delete_dlg(
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

    def show_create_task_popup(self, e):
        self._create_task_centered_container = ft.Container(
            content=self._create_task_card,
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=ft.colors.with_opacity(0.7, ft.colors.BLACK),
        )
        if self.page.overlay:
            self.page.overlay.pop()
            self.page.update()
        self.page.overlay.append(self._create_task_centered_container)

        self.page.update()

    def show_update_task_popup(self, task_model: TaskResponseModel):
        self._update_task_card.data = task_model.id
        formatted_date = ISO8601_to_std(task_model.due_date)
        self._update_task_card._title_textfield.value = task_model.title
        self._update_task_card._description_textfield.value = task_model.description
        self._update_task_card._due_date_cal.value = task_model.due_date
        self._update_task_card._due_date_text_field.value = formatted_date
        self.page.update()

        self._update_task_centered_container = ft.Container(
            content=self._update_task_card,
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=ft.colors.with_opacity(0.7, ft.colors.BLACK),
        )
        if self.page.overlay:
            self.page.overlay.pop()
            self.page.update()
        self.page.overlay.append(self._update_task_centered_container)

        self.page.update()

    def build(self) -> ft.Control:
        self.__build_content = ft.ListView(
            controls=[],
            spacing=10,
        )

        return self.__build_content
