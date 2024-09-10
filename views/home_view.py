import flet as ft


class HomeView(ft.UserControl):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.page = page

    def build(self):
        # Body content
        content = ft.Column(
            controls=[
                ft.Text("This is the main content of the homepage.", size=16),
                ft.ElevatedButton("Click Me", on_click=self.on_button_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )

        # Returning the page layout
        return ft.Column(controls=[content], expand=True)

    def on_button_click(self, e):
        self.page.go("/login")
        self.update()
