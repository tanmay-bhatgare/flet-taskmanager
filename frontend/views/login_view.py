import time
import flet as ft
import httpx
import pydantic
from icecream import ic

# * custom imports
from constants.constants import (
    WidgetStyle,
    CustomPalette,
    Urls,
    Routes,
    SessionKey,
    TailWindColors,
)
from controllers.controllers import LoginController
from models.models import LoginModel
from utils.jwt_token_encoder import encrypt_jwt
from utils.field_error_updater import set_field_error_if_empty
from utils.session_storage_setter import (
    async_get_session_value,
    async_set_session_value,
)
from widgets.widgets import CElevatedButton
from constants.constants import fonts

ic.configureOutput(prefix="Debug | ", includeContext=True)


class LoginView(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.page = page
        self.page.fonts = {
            fonts.Kanit.fontName: fonts.Kanit.fontURL,
            fonts.JetBrainsMono.fontName: fonts.JetBrainsMono.fontURL,
        }
        self.page.theme = ft.Theme(font_family=fonts.Kanit.fontName)
        self.controller = LoginController(url=Urls.login_url)
        self.__snack_bar = ft.SnackBar(
            content=ft.Text(
                "Login Successful, Enjoy!", color=CustomPalette.dark_text_color
            ),
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=6,
            dismiss_direction=ft.DismissDirection.HORIZONTAL,
            behavior=ft.SnackBarBehavior.FLOATING,
        )

        self.animate = ft.animation.Animation(2000, ft.AnimationCurve.BOUNCE_OUT)
        self.height = 0
        self.opacity = 0.5
        self.border_radius = 8
        self.bgcolor = "#14181B"
        self.border = ft.border.all(width=1, color=TailWindColors.emerald_200)

        # Email and password fields
        self.email_field = ft.TextField(
            value="t1@g.com",
            label="E-mail",
            hint_text="Enter your email",
            width=self.page.width * 0.9,
            hint_style=WidgetStyle.input_field_style(
                color=CustomPalette.light_text_color, size=16
            ),
            label_style=WidgetStyle.input_field_style(
                color=CustomPalette.light_text_color, size=16
            ),
            color=CustomPalette.light_text_color,
            border_color=TailWindColors.teal_100,
            on_focus=lambda _: self.clear_err_text(self.email_field),
        )
        self.password_field = ft.TextField(
            value="12",
            label="Password",
            hint_text="Enter your password",
            width=self.page.width * 0.9,
            password=True,
            can_reveal_password=True,
            hint_style=WidgetStyle.input_field_style(
                color=CustomPalette.light_text_color, size=16
            ),
            label_style=WidgetStyle.input_field_style(
                color=CustomPalette.light_text_color, size=16
            ),
            color=CustomPalette.light_text_color,
            border_color=TailWindColors.teal_100,
            on_submit=self.on_login_click,
            on_focus=lambda _: self.clear_err_text(self.password_field),
        )
        self.login_button = CElevatedButton(
            button_content=ft.Text("Log In", scale=2),
            on_click=self.on_login_click,
            elevation=5,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                color=TailWindColors.slate_100,
                bgcolor="#161a1d",
            ),
        )

        # Add the content directly to the container
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    margin=ft.margin.only(top=10, bottom=5),
                    content=ft.Text(
                        "Log In",
                        size=45,
                        color=TailWindColors.slate_200,
                        font_family=fonts.Kanit.fontName,
                        text_align=ft.TextAlign.CENTER,
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
                                                "Sign Up",
                                                ft.TextStyle(
                                                    color=TailWindColors.emerald_200,
                                                    weight=ft.FontWeight.W_800,
                                                ),
                                                on_click=lambda _: self.page.go(
                                                    Routes.sign_up_route
                                                ),
                                            ),
                                        ],
                                        italic=True,
                                        color=TailWindColors.slate_200,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    margin=ft.margin.only(bottom=20),
                ),
                ft.Container(
                    border=ft.border.all(width=1, color=TailWindColors.teal_100),
                    padding=0,
                    margin=0,
                    border_radius=8,
                    content=self.login_button,
                    width=110,
                    height=50,
                ),
                ft.Container(height=2),
                ft.Text(
                    "Aagaya Bhai Wapis! Chal Jaldi Kar.",
                    style=ft.TextStyle(size=12),
                    italic=True,
                    color=TailWindColors.green_200,
                ),
            ],
        )

    async def on_login_click(self, e):
        current_time = time.time()
        ic("Login Function Triggered!!!")

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
                    await async_set_session_value(
                        page=self.page,
                        key=SessionKey.login_timestamp,
                        value=current_time,
                    )
                    ic(
                        "Login Successful! At:",
                        await async_get_session_value(
                            page=self.page, key=SessionKey.login_timestamp
                        ),
                    )
                except Exception:
                    ic("Failed To Store Token")

                self.disable_card_state(state=False)
                self.show_snack_bar("Login Successful. Su Swagatam!🙏", floating=False)
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
        except httpx.RequestError as e:
            self.show_snack_bar("Unable to Connect to Server", italic=False)
            ic("Unable to Conncet to server", e)
        except Exception as e:
            ic("Overall Exception", e)
        finally:
            self.disable_card_state(state=False)

    def disable_card_state(self, state: bool):
        self.disabled = state
        self.update()

    def show_snack_bar(
        self,
        message: str,
        text_color: str = TailWindColors.slate_100,
        bgcolor: str = TailWindColors.gray_800,
        size: int = 15,
        italic: bool = True,
        floating: bool = True,
    ):
        self.__snack_bar.bgcolor = bgcolor
        self.__snack_bar.content.color = text_color
        self.__snack_bar.content.size = size
        self.__snack_bar.content.italic = italic
        self.__snack_bar.content.value = message
        self.__snack_bar.behavior = (
            ft.SnackBarBehavior.FLOATING if floating else ft.SnackBarBehavior.FIXED
        )
        self.page.snack_bar = self.__snack_bar
        self.page.snack_bar.open = True
        self.page.update()

    def did_mount(self):
        time.sleep(0.09)
        self.height = self.page.height * 0.41
        self.opacity = 1
        self.update()

    @staticmethod
    def clear_err_text(field: ft.TextField):
        field.error_text = ""
        field.update()
