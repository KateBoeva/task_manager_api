import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator


class RequestSchema(BaseModel):
    # PostgreSQL не может хранить символ NUL в текстовых полях
    @field_validator("*")
    @classmethod
    def reject_nul(cls, value):
        if isinstance(value, str) and "\x00" in value:
            raise ValueError("NUL characters are not allowed")

        return value


class TaskCreate(RequestSchema):
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]
    description: str | None = None
    priority_id: int
    status_id: int


class TaskDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status_id: int
    priority_id: int
    created_at: datetime.datetime


class StatusDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class StatusCreateUpdate(RequestSchema):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=30)]
