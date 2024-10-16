import time
import flet as ft


class CContainer(ft.Container):
    def __init__(self):
        super().__init__(height=200, width=200, bgcolor="red")
        self.animate = ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT)

    def _animate(self):
        self.width = 500
        self.height = 500
        self.bgcolor = "purple"
        self.page.update()

    def did_mount(self):
        time.sleep(2)
        self._animate()
        pass


def main(page: ft.Page):
    page.add(CContainer())


ft.app(target=main)
