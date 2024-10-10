from typing import Optional
from pydantic import BaseModel

class TokenData(BaseModel):
    id: Optional[int] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str