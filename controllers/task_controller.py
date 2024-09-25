from typing import Any, Dict
import httpx
from icecream import ic
from fastapi import status
from models.models import CreateTaskModel, UpdateTaskModel


ic.configureOutput(prefix="Debug | ", includeContext=True)


class TaskController:
    def __init__(self, jwt_token: str):
        self.jwt_token = jwt_token
        self.has_deleted = None
        self.has_created = None
        self.has_updated = None

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
            self.is_logged_in = False
        except httpx.RequestError as e:
            ic("Request error occurred.", e)
            self.is_logged_in = False
        except Exception as e:
            ic("An Error has occurred.", e)
            self.is_logged_in = False
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
            self.is_logged_in = False
        except httpx.RequestError as e:
            ic("Request error occurred.", e)
            self.is_logged_in = False
        except Exception as e:
            ic("An Error has occurred.", e)
            self.is_logged_in = False
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
                    self.has_created = True
                    ic(response.json())
        except httpx.HTTPStatusError:
            ic("Unable to send request.")
            self.has_created = False
        except httpx.RequestError:
            ic("Request error occurred.")
            self.has_created = False
        except Exception:
            ic("An Error has occurred.")
            self.has_created = False
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
                    self.has_deleted = True
                    ic(response.json())
        except httpx.HTTPStatusError:
            ic("Unable to send request.")
            self.has_deleted = False
        except httpx.RequestError:
            ic("Request error occurred.")
            self.has_deleted = False
        except Exception:
            ic("An Error has occurred.")
            self.has_deleted = False
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
                    self.has_updated = True
                    ic(response.json())
        except httpx.HTTPStatusError:
            ic("Unable to send request.")
            self.has_updated = False
        except httpx.RequestError:
            ic("Request error occurred.")
            self.has_updated = False
        except Exception:
            ic("An Error has occurred.")
            self.has_updated = False
        finally:
            ic("Reached Finally")
