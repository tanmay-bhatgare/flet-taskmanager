from typing import Any, Dict
import httpx
from icecream import ic
from fastapi import status
from models.models import CreateTaskModel, UpdateTaskModel


ic.configureOutput(prefix="Debug | ", includeContext=True)


class TaskController:
    def __init__(self, jwt_token: str):
        self.jwt_token = jwt_token

    async def get_tasks(self, url: str) -> Dict[str, Any] | None:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=url,
                    follow_redirects=True,
                    headers={
                        "Authorization": f"Bearer {self.jwt_token}",
                    },
                )
                if response.status_code == status.HTTP_200_OK:
                    return response.json()
                else:
                    return None
        except httpx.HTTPStatusError as e:
            ic("Unable to send request.", e)
        except httpx.RequestError as e:
            ic("Request error occurred.", e)
        except Exception as e:
            ic("An Error has occurred.", e)
        finally:
            ic("Reached Finally")

    async def get_single_task(self, url: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=url,
                    follow_redirects=True,
                    headers={
                        "Authorization": f"Bearer {self.jwt_token}",
                    },
                )
                if response.status_code == status.HTTP_200_OK:
                    return response.json()
                else:
                    return None
        except httpx.HTTPStatusError as e:
            ic("Unable to send request.", e)
        except httpx.RequestError as e:
            ic("Request error occurred.", e)
        except Exception as e:
            ic("An Error has occurred.", e)
        finally:
            ic("Reached Finally")

    async def create_task(self, url: str, task_data: CreateTaskModel):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url=url,
                    follow_redirects=True,
                    headers={
                        "Authorization": f"Bearer {self.jwt_token}",
                    },
                    json=task_data.model_dump(),
                )
                if response.status_code == status.HTTP_201_CREATED:
                    return True
                else:
                    ic(response.json())
                    return False
        except httpx.HTTPStatusError as e:
            ic("Unable to send request.", e)
            return False
        except httpx.RequestError as e:
            ic("Request error occurred.", e)
            return False
        except Exception as e:
            ic("An Error has occurred.", e)
            return False
        finally:
            ic("Reached Finally")

    async def delete_task(self, url: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    url=url,
                    follow_redirects=True,
                    headers={
                        "Authorization": f"Bearer {self.jwt_token}",
                    },
                )
                if response.status_code == status.HTTP_204_NO_CONTENT:
                    return True
                else:
                    ic(response.json())
                    return False
        except httpx.HTTPStatusError:
            ic("Unable to send request.")
            return False
        except httpx.RequestError:
            ic("Request error occurred.")
            return False
        except Exception:
            ic("An Error has occurred.")
            return False
        finally:
            ic("Reached Finally")

    async def update_task(self, url: str, task_data: UpdateTaskModel):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    url=url,
                    follow_redirects=True,
                    headers={
                        "Authorization": f"Bearer {self.jwt_token}",
                    },
                    json=task_data.model_dump(),
                )
                if response.status_code == status.HTTP_200_OK:
                    ic(response.json())
        except httpx.HTTPStatusError:
            ic("Unable to send request.")
        except httpx.RequestError:
            ic("Request error occurred.")
        except Exception:
            ic("An Error has occurred.")
        finally:
            ic("Reached Finally")
