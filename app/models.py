import datetime
from typing import Optional

from sqlalchemy import String, ForeignKey, DateTime, MetaData, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
    })


class Status(Base):
    __tablename__ = "status"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)

    def __repr__(self) -> str:
        return f"Status(id={self.id!r}, name={self.name!r})"


class Priority(Base):
    __tablename__ = "priority"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)

    def __repr__(self) -> str:
        return f"Priority(id={self.id!r}, name={self.name!r})"


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]]

    status_id: Mapped[int] = mapped_column(ForeignKey("status.id"), index=True)
    priority_id: Mapped[int] = mapped_column(ForeignKey("priority.id"), index=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, title={self.title!r})"
