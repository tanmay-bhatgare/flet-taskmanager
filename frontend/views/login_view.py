import math
import flet as ft
import pydantic
from icecream import ic

# * custom imports
from constants.constants import WidgetStyle, Pallet, Urls, Routes, SessionKey
from controllers.controllers import LoginController
from models.models import LoginModel
from utils.jwt_token_encoder import encrypt_jwt
from utils.field_error_updater import set_field_error_if_empty
from utils.session_storage_setter import (
    async_get_session_value,
    async_set_session_value,
)

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
            response = await self.controller.login(
                data=LoginModel(
                    username=email,
                    password=password,
                )
            )

            if self.controller.is_logged_in:
                try:
                    access_token = response["access_token"]
                    await async_set_session_value(
                        page=self.page,
                        key=SessionKey.access_token,
                        value=encrypt_jwt(access_token),
                    )
                    await async_set_session_value(
                        page=self.page,
                        key=SessionKey.is_logged_in,
                        value=True,
                    )
                except Exception:
                    ic("Failed To Store Token")

                # Set every field to enabled
                self.disable_card_state(state=False)
                self.page.snack_bar = self.__snack_bar
                self.page.snack_bar.open = True
                self.page.update()
                ic(
                    await async_get_session_value(
                        page=self.page, key=SessionKey.access_token
                    )
                )
                self.page.go(Routes.home_route)
            else:
                try:
                    self.disable_card_state(state=False)
                    error_message = response["detail"]
                    self.__snack_bar.content.value = error_message
                    self.page.snack_bar = self.__snack_bar
                    self.page.snack_bar.open = True
                    self.page.update()

                except TypeError as e:
                    ic("TypeError occurred", e)
        except pydantic.ValidationError as e:
            self.disable_card_state(state=False)
            self.email_field.error_text = "Invalid E-mail."
            self.email_field.update()
            ic("Something went wrong!", e)
        except Exception as e:
            ic("Overall Exception", e)
        finally:
            self.disable_card_state(state=False)

    def build(self):
        # Email and password fields
        self.email_field = ft.TextField(
            value="t1@g.com",
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
            value="12",
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
            on_submit=self.on_login_click,
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
            height=self.page.height * 0.55,
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
                            "Log In",
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
                        margin=ft.margin.only(bottom=20),
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
