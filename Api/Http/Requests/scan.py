from typing import Optional
import uuid

from pydantic import BaseModel, IPvAnyAddress
from pydantic import field_validator, Field
from datetime import datetime


class ScanModel(BaseModel):
    target: IPvAnyAddress
    comment: Optional[str]

    @field_validator("comment")
    def validate_comment_length(cls, value):
        if value and len(value) < 5:
            raise ValueError("Comment must be at least 5 characters long")
        return value

    @field_validator("comment")
    def validate_comment_string(cls, value):
        if not value.isalnum():
            raise ValueError("Comment can only contain alphabetical characters")
        return value

    @field_validator("target")
    def validate_target(cls, value):
        # denied_hosts = ["localhost", "127.0.0.1", "0.0.0.0"]
        denied_hosts = []
        if value in denied_hosts:
            raise "Can not scan agents"
        return value


class ScanRequestModel(BaseModel):
    scan_id: str = str(uuid.uuid4())
    scan_name: str
    scan_owner: str
    target: IPvAnyAddress
    request_datetime: datetime

    @field_validator("target")
    def validate_target(cls, value):
        if isinstance(value, IPvAnyAddress):
            return str(value)
        return value
