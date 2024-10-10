from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Boolean,
    text,
)
from ..db.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(String, nullable=False)
    is_private = Column(Boolean, server_default="TRUE", nullable=False, default=True)
    created_at = Column(DateTime, server_default=text("NOW()"), nullable=False)
    due_date = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    is_completed = Column(
        Boolean, server_default="FALSE", nullable=False, default=False
    )
