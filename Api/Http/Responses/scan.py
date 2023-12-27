from typing import List

from pydantic import BaseModel, EmailStr


class ScanResponse(BaseModel):
    message: str
    date: str


class ResponseModel(BaseModel):
    status: str
    result: List[ScanResponse] = []


class BaseResponse(BaseModel):
    status: str
    message: str
    result: str
