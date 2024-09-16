import flet as ft
from typing import NoReturn

async def set_session_value(page: ft.Page, key: str, value: str) -> NoReturn:
    await page.client_storage.set_async(key=key, value=value)

async def get_session_value(page: ft.Page, key: str) -> str | None:
    return await page.client_storage.get_async(key)

async def clear_session_vale(page: ft.Page, key: str) -> NoReturn:
    await page.client_storage.remove_async(key=key)