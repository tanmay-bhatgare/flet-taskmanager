from pydantic import EmailStr, BaseModel

class LoginModel(BaseModel):
    username: EmailStr
    password: str