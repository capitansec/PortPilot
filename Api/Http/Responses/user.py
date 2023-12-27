from typing import List

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    uuid: str
    email: EmailStr
    username: str



class ResponseModel(BaseModel):
    status: str
    message: str
    result: List[UserResponse] = []


class BaseResponse(BaseModel):
    status: str
    message: str
    result: str
