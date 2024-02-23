
from pydantic import BaseModel, EmailStr


class UserRegisterBase(BaseModel):
    username: str
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "username",
                    "email": "username@mail.com",
                    "password": "password",
                }
            ]
        }
    }


class UserLoginBase(BaseModel):
    username: str
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "username",
                    "password": "password",
                }
            ]
        }
    }
