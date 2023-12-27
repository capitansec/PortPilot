from typing import Optional

from pydantic import BaseModel, EmailStr


class UserRegisterBase(BaseModel):
    username: str
    email: EmailStr
    password: Optional[str] = None


class UserLoginBase(BaseModel):
    username: str
    password: str
