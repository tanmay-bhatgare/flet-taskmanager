import time
import flet as ft
import httpx
import pydantic
from icecream import ic

# * custom imports
from constants.constants import WidgetStyle, CustomPalette, Urls, Routes, TailWindColors
from controllers.controllers import SignUpController
from models.models import SignUpModel
from utils.field_error_updater import set_field_error_if_empty
from widgets.widgets import CElevatedButton

ic.configureOutput(prefix="Debug | ", includeContext=True)


class SignUpView(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.animate = ft.animation.Animation(2000, ft.AnimationCurve.BOUNCE_OUT)
        self.page = page
        self.controller = SignUpController(url=Urls.sign_up_url)

        self.opacity = 0.5
        self.height = 0
        self.border_radius = 8
        self.bgcolor = "#14181B"
        self.border = ft.border.all(width=1, color=TailWindColors.emerald_200)

        self.__snack_bar = ft.SnackBar(
            content=ft.Text("", color=CustomPalette.dark_text_color),
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=6,
            dismiss_direction=ft.DismissDirection.HORIZONTAL,
            behavior=ft.SnackBarBehavior.FLOATING,
        )

        # Initialize email, password, confirm_password fields
        self.username_field = ft.TextField(
            on_focus=lambda _: self.clear_err_text(self.username_field),
            label="Username",
            hint_text="Choose your username",
            width=self.page.width * 0.9,
            hint_style=WidgetStyle.input_field_style(
                color=CustomPalette.light_text_color, size=16
            ),
            label_style=WidgetStyle.input_field_style(
                color=CustomPalette.light_text_color, size=16
            ),
            color=CustomPalette.light_text_color,
            border_color=TailWindColors.teal_100,
            max_length=18,
        )
        self.email_field = ft.TextField(
            on_focus=lambda _: self.clear_err_text(self.email_field),
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
        )
        self.password_field = ft.TextField(
            on_focus=lambda _: self.clear_err_text(self.password_field),
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
        )
        self.confirm_password_field = ft.TextField(
            on_focus=lambda _: self.clear_err_text(self.confirm_password_field),
            label="Confirm Password",
            hint_text="Re-enter your password",
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
        )
        self.sign_in_button = CElevatedButton(
            button_content=ft.Text("Sign Up", scale=1.5),
            on_click=self.on_signup_click,
            elevation=5,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                color=TailWindColors.slate_100,
                bgcolor="#161a1d",
            ),
        )

        # Set up the container layout
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    margin=ft.margin.only(bottom=5),
                    content=ft.Text(
                        "Sign Up",
                        weight=ft.FontWeight.BOLD,
                        size=45,
                        color=TailWindColors.slate_100,
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
                                            ft.TextSpan("Already Have an Account? "),
                                            ft.TextSpan(
                                                "Sign In",
                                                ft.TextStyle(
                                                    color=TailWindColors.emerald_200,
                                                    weight=ft.FontWeight.W_800,
                                                ),
                                                on_click=lambda _: self.page.go(
                                                    Routes.login_route
                                                ),
                                            ),
                                        ],
                                        color=TailWindColors.slate_200,
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    border=ft.border.all(width=1, color=TailWindColors.teal_100),
                    padding=0,
                    margin=0,
                    border_radius=8,
                    content=self.sign_in_button,
                    width=110,
                    height=50,
                ),
                ft.Container(height=2),
                ft.Text(
                    "Naya Bhai Aagaya!🥳",
                    style=ft.TextStyle(size=12),
                    italic=True,
                    color=TailWindColors.green_200,
                ),
            ],
        )

    async def on_signup_click(self, e):
        ic("Sign up Function Triggered!!!")

        # Storing form inputs
        username = self.username_field.value
        email = self.email_field.value
        password = self.password_field.value
        confirm_password = self.confirm_password_field.value

        # Check if any field is empty and show relevant error messages
        if set_field_error_if_empty(self.username_field, "Username is required."):
            return
        if set_field_error_if_empty(self.email_field, "E-mail is required."):
            return
        if set_field_error_if_empty(self.password_field, "Password is required."):
            return

        # Check if passwords match, if not, show error and exit
        if not self.check_password_match(
            password=password, confirm_password=confirm_password
        ):
            self.confirm_password_field.error_text = "Password does not match."
            self.confirm_password_field.update()
            return

        # Disable form only if all fields are valid and passwords match
        self.disable_card_state(state=True)

        try:
            # Call the controller's sign-up function, passing the sign-up data
            response = await self.controller.sign_up(
                data=SignUpModel(
                    username=username,
                    email=email,
                    password=password,
                )
            )

            # Check if the user successfully signed up
            if self.controller.has_signed_up:
                self.disable_card_state(state=False)
                self.show_snack_bar(
                    message="Sign Up Successful! Please Log In.", size=14
                )

                # Navigate to login route after successful sign-up
                if (
                    self.page.route != Routes.login_route
                ):  # Only navigate if not already there
                    self.page.go(Routes.login_route)
            else:
                # Handle the case where sign-up fails for some reason
                self.disable_card_state(state=False)
                self.show_snack_bar(
                    message=response.get("detail", "Sign-up failed."), size=14
                )

        except pydantic.ValidationError as e:
            self.disable_card_state(state=False)
            self.show_snack_bar(message="Invalid E-mail format.", size=14)
            ic("Validation Error", e)

        except httpx.RequestError as e:
            self.disable_card_state(state=False)
            self.show_snack_bar(
                message="Unable to connect to server. Please try again.", size=14
            )
            ic("Request Error", e)

        except Exception as e:
            self.disable_card_state(state=False)
            self.show_snack_bar(
                message="An unexpected error occurred. Please try again.", size=14
            )
            ic("Overall Exception", e)

        finally:
            # Always re-enable the form at the end of the process, in case of errors or success
            self.disable_card_state(state=False)

    def disable_card_state(self, state: bool):
        self.disabled = state
        self.update()

    def show_snack_bar(
        self,
        message,
        text_color=TailWindColors.slate_200,
        bgcolor=TailWindColors.gray_800,
        size=15,
        italic=True,
    ):
        self.__snack_bar.bgcolor = bgcolor
        self.__snack_bar.content.color = text_color
        self.__snack_bar.content.size = size
        self.__snack_bar.content.italic = italic
        self.__snack_bar.content.value = message
        self.page.snack_bar = self.__snack_bar
        self.page.snack_bar.open = True
        self.page.update()

    def did_mount(self):
        time.sleep(0.09)
        self.height = self.page.height * 0.55
        self.opacity = 1
        self.update()

    @staticmethod
    def check_password_match(password: str, confirm_password: str):
        return password == confirm_password

    @staticmethod
    def clear_err_text(field: ft.TextField):
        field.error_text = ""
        field.update()
