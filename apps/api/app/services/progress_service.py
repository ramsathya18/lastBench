from datetime import datetime
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.lesson import Lesson
from app.models.module import Module
from app.models.progress import LessonProgress
from app.models.enums import ProgressStatus


def set_lesson_started(db: Session, user_id: int, lesson_id: int) -> LessonProgress:
    progress = db.scalar(select(LessonProgress).where(LessonProgress.user_id == user_id, LessonProgress.lesson_id == lesson_id))
    now = datetime.utcnow()
    if not progress:
        progress = LessonProgress(
            user_id=user_id,
            lesson_id=lesson_id,
            status=ProgressStatus.IN_PROGRESS,
            started_at=now,
            last_accessed_at=now,
        )
        db.add(progress)
    else:
        if progress.status == ProgressStatus.NOT_STARTED:
            progress.status = ProgressStatus.IN_PROGRESS
            progress.started_at = progress.started_at or now
        progress.last_accessed_at = now
    db.commit()
    db.refresh(progress)
    return progress


def set_lesson_completed(db: Session, user_id: int, lesson_id: int) -> LessonProgress:
    progress = set_lesson_started(db, user_id, lesson_id)
    progress.status = ProgressStatus.COMPLETED
    progress.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(progress)
    return progress


def course_progress(db: Session, user_id: int, course_id: int):
    total_lessons = db.scalar(
        select(func.count(Lesson.id)).join(Module, Lesson.module_id == Module.id).where(Module.course_id == course_id)
    ) or 0
    completed_lessons = db.scalar(
        select(func.count(LessonProgress.id))
        .join(Lesson, LessonProgress.lesson_id == Lesson.id)
        .join(Module, Lesson.module_id == Module.id)
        .where(Module.course_id == course_id, LessonProgress.user_id == user_id, LessonProgress.status == ProgressStatus.COMPLETED)
    ) or 0
    last_lesson = db.scalar(
        select(Lesson.slug)
        .join(LessonProgress, LessonProgress.lesson_id == Lesson.id)
        .join(Module, Lesson.module_id == Module.id)
        .where(Module.course_id == course_id, LessonProgress.user_id == user_id)
        .order_by(LessonProgress.last_accessed_at.desc())
        .limit(1)
    )
    completion = (completed_lessons / total_lessons * 100) if total_lessons else 0
    return {
        "course_id": course_id,
        "completion_percent": round(completion, 2),
        "completed_lessons": completed_lessons,
        "total_lessons": total_lessons,
        "last_lesson_slug": last_lesson,
    }
