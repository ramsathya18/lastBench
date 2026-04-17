from sqlalchemy import Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.models.enums import LessonType, PublishStatus


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    summary: Mapped[str] = mapped_column(Text, default="")
    lesson_type: Mapped[LessonType] = mapped_column(Enum(LessonType), nullable=False)
    content_markdown: Mapped[str] = mapped_column(Text, default="")
    estimated_minutes: Mapped[int] = mapped_column(Integer, default=10)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[PublishStatus] = mapped_column(Enum(PublishStatus), default=PublishStatus.DRAFT)
