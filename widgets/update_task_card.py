from datetime import datetime
from typing import Callable
import flet as ft

from constants.constants import Pallet, WidgetStyle


class UpdateTaskCard(ft.Container):
    def __init__(
        self,
        title: str = None,
        description: str = None,
        is_private: bool = None,
        created_at: str | datetime = None,
        due_date: str | datetime = "2024-10-03T10:22:17.212Z",
        is_completed: bool = None,
        completed_at: str | datetime = None,
        update_function: Callable = None,
        delete_function: Callable = None,
        height: int = 320,
        width: int = 360,
        background_color: str = "red",
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
        self.on_click = lambda _: print("Container Clicked!")

        # Define the content for the container
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=3,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    height=30,
                    controls=[
                        ft.IconButton(icon=ft.icons.CLOSE, on_click=self.__self_close),
                    ]
                ),
                ft.Row(
                    controls=[
                        # Title TextField
                        ft.TextField(
                            expand=True,
                            border_color=Pallet.transparent,
                            focused_border_color=Pallet.transparent,
                            hint_text="Task Title",
                            filled=True,
                            text_size=16,
                            border_radius=7,
                        ),
                    ],
                ),
                # Description
                ft.TextField(
                    height=150,
                    min_lines=5,
                    multiline=True,
                    hint_text="Task Description",
                    hint_style=ft.TextStyle(color=Pallet.slate_grey),
                    border_color=Pallet.transparent,
                    border_radius=7,
                    filled=True,
                    hover_color=Pallet.transparent,
                ),
                ft.Column(
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                # Delete button
                                ft.ElevatedButton(
                                    text="Due: ",
                                    height=40,
                                    on_click=delete_function,
                                    style=WidgetStyle.action_button(
                                        bgcolor="#34d399",
                                        text_color="white",
                                        font_size=18,
                                        border_radius=12,
                                        weight=ft.FontWeight.BOLD,
                                        italic=True,
                                    ),
                                ),
                                # Update button
                                ft.ElevatedButton(
                                    text="Save ",
                                    height=40,
                                    on_click=update_function,
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
    def __self_close(self, e):
        self.page.overlay.pop()
        self.page.update()