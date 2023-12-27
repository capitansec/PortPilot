from typing import Optional

from pydantic import BaseModel, IPvAnyAddress, field_validator


class Scan(BaseModel):
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
        denied_hosts = ["localhost", "127.0.0.1", "0.0.0.0"]
        if value in denied_hosts:
            raise "Can not scan agents"
        return value
