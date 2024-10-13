import flet as ft
import time
import asyncio
from icecream import ic

ic.configureOutput(prefix="Debug | ", includeContext=True)


async def check_session_timeout(page: ft.Page):
    ic("Checking Session Timeout")
    while True:
        ic("In Session while loop")
        login_timestamp = await page.client_storage.get_async("login_timestamp")
        is_logged_in = await page.client_storage.get_async("is_logged_in")

        if login_timestamp is not None and is_logged_in:
            ic("condition executed")
            elapsed_time = time.time() - float(login_timestamp)
            ic(elapsed_time)
            if elapsed_time > 10:  # 3600 seconds = 60 minutes
                await page.client_storage.set_async("is_logged_in", False)
                page.update()  # Update the page if needed
                print("Session timed out. Logged out at,", time.ctime(time.time()))
        await asyncio.sleep(2)  # Check every 10 seconds (adjust this as necessary)


# Function to start a session
async def login(page: ft.Page):
    current_time = time.time()
    await page.client_storage.set_async("login_timestamp", str(current_time))
    await page.client_storage.set_async("is_logged_in", True)
    print("Logged in at:", time.ctime(current_time))


# Function to handle logout
async def logout(page):
    await page.client_storage.set_async("is_logged_in", False)
    print("Logged out manually.")
    page.update()


# Main UI logic
async def main(page: ft.Page):
    # await page.client_storage.clear_async()
    page.title = "Login Timer Example"

    # Button to simulate login
    async def on_login_click(e):
        await login(page)

    # Button to simulate manual logout
    async def on_logout_click(e):
        await logout(page)

    # UI Elements
    login_button = ft.ElevatedButton(text="Login", on_click=on_login_click)
    logout_button = ft.ElevatedButton(text="Logout", on_click=on_logout_click)

    # Add UI elements before starting the background task
    page.add(login_button, logout_button)

    # Start checking for session timeout in the background
    asyncio.create_task(check_session_timeout(page))


ft.app(target=main)
