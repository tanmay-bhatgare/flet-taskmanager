from datetime import datetime
from typing import Callable
import flet as ft

from constants.constants import Pallet, WidgetStyle
from utils.date_converter import ISO8601_to_std


class TaskCard(ft.UserControl):
    def __init__(
        self,
        title: str = None,
        description: str = None,
        is_private: bool = None,
        created_at: str | datetime = None,
        due_date: str | datetime = None,
        is_completed: bool = None,
        completed_at: str | datetime = None,
        update_function: Callable = None,
        delete_function: Callable = None,
        height: int = 280,
        width: int = 360,
        background_color: str = "red",
        **kwargs,
    ):
        super().__init__()
        self.height = height
        self.width = width
        self.background_color = background_color
        self.card_container = ft.Container(
            expand=True,
            height=self.height,
            width=self.width,
            bgcolor=self.background_color,
            border_radius=15,
            padding=ft.padding.all(8),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            # ? Title
                            ft.Text(
                                title,
                                style=ft.TextThemeStyle.TITLE_LARGE,
                                color=Pallet.light_text_color,
                                weight=ft.FontWeight.BOLD,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                width=320,
                            ),
                            # ? created date
                            ft.Text(
                                ISO8601_to_std(created_at), color=ft.colors.GREY_400
                            ),
                        ],
                    ),
                    # ? Description
                    ft.TextField(
                        height=150,
                        read_only=True,
                        min_lines=5,
                        multiline=True,
                        value=description,
                        border_color=ft.colors.TRANSPARENT,
                        border_radius=7,
                        fill_color=Pallet.card_textfield,
                        hover_color="transparent",
                    ),
                    ft.Column(
                        controls=[
                            # ? Due date
                            ft.Text(f"Due: {ISO8601_to_std(due_date)}"),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    # ? delete button
                                    ft.ElevatedButton(
                                        text="Delete ",
                                        height=40,
                                        on_click=delete_function,
                                        style=WidgetStyle.action_button(
                                            bgcolor="#ef4444",
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
                                            bgcolor=ft.colors.BLUE_700,
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
            ),
        )

    def build(self):
        return self.card_container
