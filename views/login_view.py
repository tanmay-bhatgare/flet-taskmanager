import flet as ft
import pydantic
from icecream import ic

# * custom imports
from constants.constants import WidgetStyle, Pallet, Urls
from controllers.controllers import LoginController
from models.models import LoginModel

ic.configureOutput(prefix="Debug | ", includeContext=True)


class LoginView(ft.UserControl):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.page = page
        self.controller = LoginController(url=Urls.login_url)
        self.__card_width_to_page_ratio = 1

    async def on_login_click(self, e):
        # Set every field to disabled
        self.set_card_state(state=True)
        ic("Login Function Triggered!!!")

        # Storing email and password
        email = self.email_field.value
        password = self.password_field.value

        try:
            response_json = await self.controller.login(
                data=LoginModel(
                    username=email,
                    password=password,
                )
            )

            if self.controller.is_logged_in:
                try:
                    await self.page.client_storage.set_async("taskmanager.ACCESS_TOKEN", response_json["access_token"])
                    ic("Test value set successfully")
                except Exception as e:
                    ic("Test value setting failed", e)

                # Set every field to enabled
                self.set_card_state(state=False)

                ic("Login Successful")
                self.page.go("/")
        except pydantic.ValidationError as e:
            self.set_card_state(state=False)
            ic("Something went wrong!", e)
        except Exception as e:
            ic("Overall Exception", e)
        finally:
            self.set_card_state(state=False)

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
                                                    on_click=lambda _: self.page.go(
                                                        "/"
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
        self.form_card.width = self.page.width
        return self.form_card

    def set_card_state(self, state: bool):
        self.form_card.disabled = state
        self.update()
