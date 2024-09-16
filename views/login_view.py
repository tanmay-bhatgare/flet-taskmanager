import math
import flet as ft
import pydantic
from icecream import ic

# * custom imports
from constants.constants import WidgetStyle, Pallet, Urls, Routes
from controllers.controllers import LoginController
from models.models import LoginModel
from utils.jwt_token_encoder import encrypt_jwt
from utils.field_error_updater import set_field_error_if_empty

ic.configureOutput(prefix="Debug | ", includeContext=True)


class LoginView(ft.UserControl):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.page = page
        self.controller = LoginController(url=Urls.login_url)
        self.__snack_bar = ft.SnackBar(
            content=ft.Text("Login Successful, Enjoy!", color=Pallet.dark_text_color),
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=6,
            dismiss_direction=ft.DismissDirection.HORIZONTAL,
        )

    async def on_login_click(self, e):
        # Set every field to disabled
        ic("Login Function Triggered!!!")

        # Storing email and password
        email = self.email_field.value
        password = self.password_field.value

        if set_field_error_if_empty(self.email_field, "E-mail is required."):
            return
        if set_field_error_if_empty(self.password_field, "Password is required."):
            return

        self.disable_card_state(state=True)
        try:
            response_json = await self.controller.login(
                data=LoginModel(
                    username=email,
                    password=password,
                )
            )

            if self.controller.is_logged_in:
                try:
                    access_token = response_json["access_token"]
                    await self.page.client_storage.set_async(
                        "taskmanager.ACCESS_TOKEN", encrypt_jwt(access_token)
                    )
                except Exception as e:
                    ic("Test value setting failed", e)

                # Set every field to enabled
                self.disable_card_state(state=False)
                self.page.snack_bar = self.__snack_bar
                self.page.snack_bar.open = True
                self.page.update()
                ic(await self.page.client_storage.get_async("taskmanager.ACCESS_TOKEN"))
                self.page.go(Routes.home_route)
        except pydantic.ValidationError as e:
            self.disable_card_state(state=False)
            ic("Something went wrong!", e)
        except Exception as e:
            ic("Overall Exception", e)
        finally:
            self.disable_card_state(state=False)

    def build(self):
        # Email and password fields
        self.email_field = ft.TextField(
            label="E-mail",
            hint_text="Enter your email",
            width=self.page.width * 0.9,
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
            width=self.page.width * 0.9,
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
            elevation=5,
        )

        self.form_container = ft.Container(
            height=self.page.height * 0.5,
            border_radius=8,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.Alignment(0.8, 1),
                colors=[
                    "0xff1f005c",
                    "0xff5b0060",
                ],
                tile_mode=ft.GradientTileMode.MIRROR,
                rotation=math.pi / 6,
            ),
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
                                    wrap=True,
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
                                                        Routes.sign_up_route
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
        )
        self.form_container.width = self.page.width
        return self.form_container

    def disable_card_state(self, state: bool):
        self.form_container.disabled = state
        self.update()
