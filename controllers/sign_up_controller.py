import httpx
from icecream import ic
from models.models import SignUpModel


class SignUpController:
    def __init__(self, url) -> None:
        self.url = url
        self.has_signed_up = None
        self.error_message = ""

    async def sign_up(self, data: SignUpModel)-> dict[str, str]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url=self.url,
                    json=data.model_dump(),
                )
                if response.status_code == 201:
                    self.has_signed_up = True
                    return {"detail": "Sign Up Successful! Please Log In."}

                else:
                    self.has_signed_up = False
                    return response.json()
        except httpx.HTTPStatusError:
            ic("Unable to send request.")
            self.has_signed_up = False
        except httpx.RequestError:
            ic("Request error occurred.")
            self.has_signed_up = False
        except Exception:  # ? Base Exception Case
            ic("An Error has occurred.")
            self.has_signed_up = False
        finally:
            ic("Reached Finally")
