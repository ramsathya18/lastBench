from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class SandboxTask(Base):
    __tablename__ = "sandbox_tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE"), unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    instructions: Mapped[str] = mapped_column(Text, default="")
    starter_template: Mapped[str] = mapped_column(Text, default="")
    validator_config: Mapped[dict] = mapped_column(JSON, default=dict)
    runtime_type: Mapped[str] = mapped_column(String(50), default="prompt")


class SandboxRun(Base):
    __tablename__ = "sandbox_runs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    sandbox_task_id: Mapped[int] = mapped_column(ForeignKey("sandbox_tasks.id", ondelete="CASCADE"), index=True)
    submitted_content: Mapped[str] = mapped_column(Text, default="")
    output: Mapped[str] = mapped_column(Text, default="")
    logs: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(50), default="completed")
    score_or_result: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
