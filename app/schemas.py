from pydantic import BaseModel, field_validator


class TaskCreate(BaseModel):
    title: str
    description: str
    priority: int


class StatusDetail(BaseModel):
    id: int
    name: str


class StatusCreateUpdate(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def check_name(cls, value):
        if not value:
            raise ValueError('Invalid status name')

        return value
