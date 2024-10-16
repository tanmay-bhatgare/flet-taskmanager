import flet as ft

from constants.constants import TailWindColors


class CElevatedButton(ft.ElevatedButton):
    def __init__(
        self,
        on_click: ft.TapEvent = None,
        style: ft.ButtonStyle | None = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            color=TailWindColors.slate_100,
            bgcolor="#161a1d",
        ),
        button_content: ft.Control = ft.Text("CButton"),
        elevation: int | None = 5,
        expand: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(
            content=button_content,
            on_click=on_click,
            elevation=elevation,
            expand=expand,
            style=style,
            **kwargs,
        )
