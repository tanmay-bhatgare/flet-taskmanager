import httpx

from models.models import LoginModel


class LoginController:
    def __init__(self, url) -> None:
        self.url = url
        self.username = ""
        self.is_logged_in = False
        self.error_message = ""

    async def login(self, data: LoginModel):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url=self.url, data=data.model_dump())
                if response.status_code == 200:
                    self.is_logged_in = True
                else:
                    print(response.json())
        except httpx.HTTPStatusError:
            print("Unable to send request.")
        except Exception:
            print("An Error has occurred.")
