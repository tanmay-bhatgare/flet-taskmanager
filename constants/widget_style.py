import flet as ft


class WidgetStyle:
    """A Constant Class for custom and Re-usable control styles"""

    def action_button(
        bgcolor: str = "#242a31",
        text_color: str = "black",
        border_radius: int = 5,
        padding_vertical: int = 10,
        padding_horizontal: int = 14,
        font_size: int = 23,
        weight: str = ft.FontWeight.W_600,
    ):
        return ft.ButtonStyle(
            bgcolor=bgcolor,
            color=text_color,
            shape=ft.RoundedRectangleBorder(border_radius),
            padding=ft.padding.symmetric(
                vertical=padding_vertical, horizontal=padding_horizontal
            ),
            text_style=ft.TextStyle(size=font_size, weight=weight),
        )

    def input_field_style(color, size, **kwargs):
        return ft.TextStyle(color=color, size=size, **kwargs)
