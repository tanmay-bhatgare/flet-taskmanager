from typing import Callable
import flet as ft

from constants.constants import CustomPalette, TailWindColors, WidgetStyle, fonts
from utils.date_handler import ISO8601_to_std, color_due_date
from models.models import TaskResponseModel


class TaskCard(ft.Container):
    def __init__(
        self,
        task_model: TaskResponseModel,
        update_function: Callable = None,
        delete_function: Callable = None,
        height: int = 280,
        width: int = 360,
        background_color: str = "red",
    ):
        super().__init__(
            expand=True,
            height=height,
            width=width,
            bgcolor=background_color,
            border_radius=15,
            padding=ft.padding.all(8),
        )
        self.__due_date_color, self.__due_msg = color_due_date(
            created_date=task_model.created_at,
            due_date=task_model.due_date,
        )

        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        # ? Title
                        ft.Text(
                            value=task_model.title,
                            style=ft.TextThemeStyle.TITLE_LARGE,
                            color=CustomPalette.light_text_color,
                            weight=ft.FontWeight.BOLD,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            width=width * 0.5,
                        ),
                        # ? created date
                        ft.Text(
                            value=ISO8601_to_std(task_model.created_at),
                            color=TailWindColors.gray_300,
                        ),
                    ],
                ),
                # ? Description
                ft.TextField(
                    height=150,
                    read_only=True,
                    min_lines=5,
                    multiline=True,
                    value=task_model.description,
                    border_color=ft.colors.TRANSPARENT,
                    border_radius=7,
                    fill_color=CustomPalette.card_textfield,
                    hover_color="transparent",
                    text_style=ft.TextStyle(
                        font_family=fonts.JetBrainsMono.fontName,
                        size=15,
                        color=TailWindColors.slate_200,
                    ),
                ),
                ft.Column(
                    controls=[
                        # ? Due date
                        ft.Text(
                            f"Due: {ISO8601_to_std(task_model.due_date)}",
                            font_family=fonts.JetBrainsMono.fontName,
                            size=12,
                            tooltip=self.__due_msg,
                            color=self.__due_date_color,
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                # ? delete button
                                ft.ElevatedButton(
                                    text="Delete ",
                                    height=40,
                                    on_click=delete_function,
                                    style=WidgetStyle.action_button(
                                        bgcolor=TailWindColors.rose_600,
                                        text_color="white",
                                        font_size=18,
                                        border_radius=12,
                                        weight=ft.FontWeight.BOLD,
                                        italic=True,
                                    ),
                                ),
                                ft.Container(width=10),
                                # ? update button
                                ft.ElevatedButton(
                                    text="Update ",
                                    height=40,
                                    on_click=update_function,
                                    style=WidgetStyle.action_button(
                                        bgcolor=TailWindColors.blue_800,
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
