import flet as ft


def set_field_error_if_empty(field: ft.TextField, message: str)->bool:
    if not field.value.strip():
        field.error_text = message
        field.update()
        return True
    else:
        field.error_text = None
        field.update()
        return False
