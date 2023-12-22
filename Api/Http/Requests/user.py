from typing import Optional

from pydantic import BaseModel, EmailStr


class UserRegisterBase(BaseModel):
    full_name: Optional[str] = None
    username: str
    email: EmailStr
    password: Optional[str] = None


class UserLoginBase(BaseModel):
    username: str
    password: str
