import asyncio
import time
import flet as ft
from icecream import ic

from constants.constants import Routes

ic.configureOutput(prefix="Debug => ", includeContext=True)


async def check_session_timeout(
    page: ft.Page,
    login_timestamp_key: str,
    is_logged_in_key: str,
    session_timeout_min: float,
    delay: int = 2,
    navigate_to: str = Routes.login_route,
):
    ic("Checking Session Timeout Triggered")
    while True:
        # ic("In Session while loop")
        is_logged_in = await page.client_storage.get_async(is_logged_in_key)
        login_timestamp = await page.client_storage.get_async(login_timestamp_key)


        if login_timestamp is not None and is_logged_in:
            elapsed_time = time.time() - float(login_timestamp)

            if elapsed_time > session_timeout_min * 60:
                ic("Condition executed")
                await page.client_storage.set_async(is_logged_in_key, False)
                page.go(navigate_to)
                page.update()
                ic("Logged User Out as it's been, ", elapsed_time)

        await asyncio.sleep(delay=delay)
