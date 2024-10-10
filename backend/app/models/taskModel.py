import enum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, text, Enum
from ..db.database import Base


class TaskStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Task(Base):

    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(String, nullable=False)
    status = Column(Enum(TaskStatus, values_callable=lambda obj: [
                    e.value for e in obj]), server_default=TaskStatus.PENDING.value, default=TaskStatus.PENDING.value)
    is_private = Column(Boolean, server_default="TRUE",
                        nullable=False, default=True)
    created_at = Column(DateTime, server_default=text("NOW()"), nullable=False)
    due_date = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
