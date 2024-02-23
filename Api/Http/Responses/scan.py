from typing import List, Dict, Any

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

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "status of activity result",
                    "message": "message for activity, frontend notifications",
                    "result": "expected values from activity"
                }
            ]
        }
    }


class BaseResponseScan(BaseModel):
    status: str
    message: str
    result: Dict[str, Any]