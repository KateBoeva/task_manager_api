import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
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


class StatusCreateUpdate(BaseModel):
    name: str = Field(max_length=30)

    @field_validator('name')
    @classmethod
    def check_name(cls, value):
        if not value:
            raise ValueError('Invalid status name')

        return value
