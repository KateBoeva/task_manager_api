from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str
    priority: int


class StatusDetail(BaseModel):
    id: int
    name: str


class StatusCreate(BaseModel):
    name: str
