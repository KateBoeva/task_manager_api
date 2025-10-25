from pydantic import BaseModel


class TaskCreateUpdate(BaseModel):
    title: str
    description: str
    priority: int
