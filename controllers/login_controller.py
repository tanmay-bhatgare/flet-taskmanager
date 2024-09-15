import httpx
from models.models import LoginModel
from icecream import ic

ic.configureOutput(prefix="Debug | ", includeContext=True)


class LoginController:
    def __init__(self, url) -> None:
        self.url = url
        self.is_logged_in = False
        self.error_message = ""

    async def login(self, data: LoginModel):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url=self.url,
                    data=data.model_dump(),
                )
                if response.status_code == 200:
                    self.is_logged_in = True
                    return response.json()
                else:
                    ic(response.json())
                    self.is_logged_in = False
        except httpx.HTTPStatusError:
            ic("Unable to send request.")
            self.is_logged_in = False
        except httpx.RequestError:
            ic("Request error occurred.")
            self.is_logged_in = False
        except Exception:
            ic("An Error has occurred.")
            self.is_logged_in = False
        finally:
            ic("Reached Finally")
