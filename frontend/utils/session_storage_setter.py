import flet as ft
from typing import NoReturn


async def async_set_session_value(page: ft.Page, key: str, value: str) -> NoReturn:
    await page.client_storage.set_async(key=key, value=value)


async def async_get_session_value(page: ft.Page, key: str) -> str | None:
    return await page.client_storage.get_async(key)


async def async_clear_session_vale(page: ft.Page, key: str) -> NoReturn:
    await page.client_storage.remove_async(key=key)


def set_session_value(page: ft.Page, key: str, value: str) -> NoReturn:
    page.client_storage.set(key=key, value=value)


def get_session_value(page: ft.Page, key: str) -> str | None:
    return page.client_storage.get(key)


def clear_session_vale(page: ft.Page, key: str) -> NoReturn:
    page.client_storage.remove(key=key)
