import datetime as dt
from datetime import datetime
from typing import Any, Callable, Literal
import flet as ft

from constants.constants import Pallet, WidgetStyle
from utils.date_converter import ISO8601_to_std, str_to_datetime
from models.models import CreateTaskModel, UpdateTaskModel


class PopUpTaskCard(ft.Container):
    def __init__(
        self,
        type: Literal["create", "update"] = None,
        data: Any | None = None,
        height: int = 360,
        width: int = 360,
        background_color: str = "red",
        submit_function: Callable = None,
        **kwargs,
    ):
        # Initialize the parent Container
        super().__init__(
            expand=True,
            height=height,
            width=width,
            bgcolor=background_color,
            border_radius=15,
            padding=ft.padding.all(8),
            **kwargs,
        )
        self._type: Literal["create"] | Literal["update"] = type
        self._data: Any | None = data
        self._due_date_cal = ft.DatePicker(
            value=datetime.now().isoformat(),
            first_date=datetime.now(),
            last_date=datetime.now() + dt.timedelta(days=365 * 5),
            on_change=self.__due_date_change,
        )
        self._due_date_text_field = ft.Text(
            f"{ISO8601_to_std(self._due_date_cal.value)}"
        )
        self._title_textfield = ft.TextField(
            expand=True,
            border_color=Pallet.transparent,
            focused_border_color=Pallet.transparent,
            hint_text="Task Title",
            filled=True,
            text_size=16,
            border_radius=7,
            autocorrect=True,
            max_length=50,
        )
        self._description_textfield = ft.TextField(
            height=150,
            min_lines=5,
            multiline=True,
            hint_text="Task Description",
            hint_style=ft.TextStyle(color=Pallet.slate_grey),
            border_color=Pallet.transparent,
            border_radius=7,
            filled=True,
            # hover_color=Pallet.transparent,
            autocorrect=True,
        )

        # Define the content for the container
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=3,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.IconButton(icon=ft.icons.CLOSE, on_click=self._self_close),
                    ],
                ),
                ft.Row(
                    controls=[
                        # Title TextField
                        self._title_textfield,
                    ],
                ),
                # Description
                self._description_textfield,
                # Due Date
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.Text("Due Date: "),
                        self._due_date_text_field,
                    ],
                ),
                ft.Column(
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                # Delete button
                                ft.IconButton(
                                    width=40,
                                    icon=ft.icons.CALENDAR_MONTH,
                                    icon_color="#111827",
                                    tooltip="Due date",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=6),
                                        bgcolor="#34d399",
                                    ),
                                    on_click=lambda _: self.page.open(
                                        self._due_date_cal,
                                    ),
                                ),
                                # Update button
                                ft.ElevatedButton(
                                    text="Set Task "
                                    if self._type == "create"
                                    else "Update ",
                                    height=40,
                                    on_click=submit_function
                                    if submit_function
                                    else lambda _: print(self.return_data()),
                                    style=WidgetStyle.action_button(
                                        bgcolor="#3b82f6",
                                        text_color="white",
                                        font_size=18,
                                        border_radius=12,
                                        weight=ft.FontWeight.BOLD,
                                        italic=True,
                                        padding_horizontal=20,
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    def _self_close(self, e):
        self.page.overlay.pop()
        self.page.update()

    def __due_date_change(self, e):
        self._due_date_text_field.value = f"{ISO8601_to_std(self._due_date_cal.value)}"
        self._due_date_text_field.update()

    def return_data(self) -> CreateTaskModel | UpdateTaskModel | None:
        title = self._title_textfield.value
        description = self._description_textfield.value
        due_date = self._due_date_text_field.value
        due_date_iso = str_to_datetime(due_date).isoformat()

        if self._type == "create":
            return CreateTaskModel(
                title=title,
                description=description,
                is_private=True,  #! This Is hard coded value
                due_date=due_date_iso,
            )
        elif self._type == "update":
            return UpdateTaskModel(
                title=title,
                description=description,
                due_date=due_date_iso,
                is_private=True,  #! This Is hard coded value
                is_completed=False,  #! This Is hard coded value
            )
