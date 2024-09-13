import flet as ft

class SignUpView(ft.UserControl):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.page = page
        
    def build(self):
        return ft.Text("Sign Up View", size=40, text_align=ft.TextAlign.CENTER)