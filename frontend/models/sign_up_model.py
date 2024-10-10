from pydantic import EmailStr, BaseModel

class SignUpModel(BaseModel):
    username: str
    email: EmailStr
    password: str