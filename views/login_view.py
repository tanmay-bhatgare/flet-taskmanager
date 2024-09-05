import flet as ft

# * custom imports
from constants.constants import WidgetStyle, Pallet, Urls
from controllers.controllers import LoginController
from models.models import LoginModel


class LoginView(ft.UserControl):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.page = page
        self.controller = LoginController(url=Urls.login_url)
        self.__card_width_to_page_ratio = 0.5

    async def on_login_click(self, e):
        # settiing every field to disabled
        self.form_card.disabled = True
        self.update()

        print("Login Function Triggred!!!")

        # ? Stroing email and password
        email = self.email_field.value
        password = self.password_field.value

        try:
            await self.controller.login(
                data=LoginModel(
                    username=email,
                    password=password,
                )
            )

            if self.controller.is_logged_in:
                # ? Setting controller's username variable to email
                self.controller.username = self.email_field.value

                # ? setting every field to enabled
                self.form_card.disabled = False
                self.update()

                print("Login Successful")
        except Exception:
            self.form_card.disabled = False
            self.update()

            print("Something went wrong!")

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
        self.login_button = ft.ElevatedButton(
            text="Log In",
            style=WidgetStyle.action_button(
                text_color="#242524",
                weight=ft.FontWeight.W_700,
                bgcolor=ft.colors.GREY_400,
            ),
            on_click=self.on_login_click,
        )

        self.form_card = ft.Card(
            color=Pallet.royal_purple,
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
                    self.login_button,
                ],
            ),
            shadow_color=ft.colors.SURFACE_VARIANT,
        )

        return self.form_card
