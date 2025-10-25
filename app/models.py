import datetime
from typing import Optional, List

from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]]

    status_id: Mapped[int] = mapped_column(ForeignKey("Status.id"))
    priority_id: Mapped[int] = mapped_column(ForeignKey("Priority.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, title={self.title!r})"


class Status:
    __tablename__ = "status"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Status(id={self.id!r}, name={self.name!r})"


class Priority:
    __tablename__ = "priority"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Priority(id={self.id!r}, name={self.name!r})"
