import flet as ft
import pydantic
from icecream import ic

# * custom imports
from constants.constants import WidgetStyle, Pallet, Urls, Routes
from controllers.controllers import SignUpController
from models.models import SignUpModel
from utils.field_error_updater import set_field_error_if_empty
ic.configureOutput(prefix="Debug | ", includeContext=True)


class SignUpView(ft.UserControl):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.page = page
        self.controller = SignUpController(url=Urls.sign_up_url)
        self.__snack_bar = ft.SnackBar(
            content=ft.Text(
                "Sign Up Successful! Please Log In.", color=Pallet.dark_text_color
            ),
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=6,
            dismiss_direction=ft.DismissDirection.HORIZONTAL,
        )

    async def on_signup_click(self, e):
        # Set every field to disabled
        ic("Sign up Function Triggered!!!")

        # Storing email and password
        username = self.username_field.value
        email = self.email_field.value
        password = self.password_field.value
        confirm_password = self.confirm_password_field.value

        if set_field_error_if_empty(self.username_field, "Username is required."):
            return
        if set_field_error_if_empty(self.email_field, "E-mail is required."):
            return
        if set_field_error_if_empty(self.password_field, "Password is required."):
            return

        # ? Password Matching Block
        if not self.check_password_match(
            password=password, confirm_password=confirm_password
        ):
            self.confirm_password_field.error_text = "Password does not match."
            self.confirm_password_field.update()
            return

        self.disable_card_state(state=True)
        try:
            await self.controller.sign_up(
                data=SignUpModel(
                    username=username,
                    email=email,
                    password=password,
                )
            )

            if self.controller.has_signed_up:
                # Set every field to enabled
                self.disable_card_state(state=False)
                self.page.snack_bar = self.__snack_bar
                self.page.snack_bar.open = True
                self.page.update()
                self.page.go(Routes.login_route)
        except pydantic.ValidationError as e:
            self.disable_card_state(state=False)
            ic("Something went wrong!", e)
        except Exception as e:
            ic("Overall Exception", e)
        finally:
            self.disable_card_state(state=False)

    def build(self):
        # Email and password fields
        self.username_field = ft.TextField(
            label="Username",
            hint_text="Choose your username",
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
        self.confirm_password_field = ft.TextField(
            label="Confirm Password",
            hint_text="Re-enter your password",
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
        self.sign_in_button = ft.ElevatedButton(
            text="Sign In",
            style=WidgetStyle.action_button(
                text_color="#242524",
                weight=ft.FontWeight.W_700,
                bgcolor=ft.colors.GREY_400,
            ),
            on_click=self.on_signup_click,
        )

        self.form_card = ft.Card(
            color=Pallet.royal_purple,
            width=self.page.width,
            height=self.page.height * 0.7,
            elevation=8,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        margin=ft.margin.only(bottom=30),
                        content=ft.Text(
                            "Sign In",
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
                                self.username_field,
                                self.email_field,
                                self.password_field,
                                self.confirm_password_field,
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    wrap=True,
                                    controls=[
                                        ft.Text(
                                            spans=[
                                                ft.TextSpan(
                                                    "Already Have an Account? "
                                                ),
                                                ft.TextSpan(
                                                    "Sign In.",
                                                    ft.TextStyle(
                                                        color=Pallet.secondary_color,
                                                        italic=True,
                                                        weight=ft.FontWeight.BOLD,
                                                    ),
                                                    on_click=lambda _: self.page.go(
                                                        Routes.login_route
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
                    self.sign_in_button,
                ],
            ),
            shadow_color=ft.colors.SURFACE_VARIANT,
        )
        return self.form_card

    def disable_card_state(self, state: bool):
        self.form_card.disabled = state
        self.update()

    @staticmethod
    def check_password_match(password: str, confirm_password: str):
        return password == confirm_password