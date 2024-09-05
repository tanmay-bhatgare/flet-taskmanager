import flet as ft
from constants.constants import WidgetStyle, Pallet


class LoginView(ft.UserControl):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.page = page
        self.__card_width_to_page_ratio = 0.5

    def build(self):
        # Email and password fields
        self.email_field = ft.TextField(
            label="E-mail",
            hint_text="Enter your email",
            width=(self.page.width * self.__card_width_to_page_ratio) * 0.9,
            hint_style=WidgetStyle.input_field_style(
                color=Pallet.light_text_color, size=16
            ),
            label_style=WidgetStyle.input_field_style(
                color=Pallet.light_text_color, size=16
            ),
            color=Pallet.light_text_color,
            border_color="white",
        )
        self.password_field = ft.TextField(
            label="Password",
            hint_text="Enter your password",
            width=(self.page.width * self.__card_width_to_page_ratio) * 0.9,
            password=True,
            can_reveal_password=True,
            hint_style=WidgetStyle.input_field_style(
                color=Pallet.light_text_color, size=16
            ),
            label_style=WidgetStyle.input_field_style(
                color=Pallet.light_text_color, size=16
            ),
            color=Pallet.light_text_color,
            border_color="white",
        )

        return ft.Card(
            color=Pallet.violet,
            width=self.page.width * self.__card_width_to_page_ratio,
            height=self.page.height * 0.55,
            elevation=8,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        margin=ft.margin.only(bottom=30),
                        content=ft.Text(
                            "Login",
                            weight=ft.FontWeight.BOLD,
                            size=45,
                            color="white",
                            italic=True,
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(vertical=20, horizontal=20),
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                self.email_field,
                                self.password_field,
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text(
                                            spans=[
                                                ft.TextSpan("Don't Have an Account? "),
                                                ft.TextSpan(
                                                    "Sign Up.",
                                                    ft.TextStyle(
                                                        color=Pallet.secondary_color,
                                                        italic=True,
                                                        weight=ft.FontWeight.BOLD,
                                                    ),
                                                    on_click=lambda _: print(
                                                        "I Have To Sign Up."
                                                    ),
                                                ),
                                            ],
                                            color="white",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    ft.ElevatedButton(
                        text="Log In",
                        style=WidgetStyle.action_button(
                            text_color="#242524",
                            weight=ft.FontWeight.W_700,
                            bgcolor=ft.colors.GREY_400
                        ),
                        on_click=lambda _: print("Log In Clicked"),
                    ),
                ],
            ),
            shadow_color=ft.colors.SURFACE_VARIANT,
        )
