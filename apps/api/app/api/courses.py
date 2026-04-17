from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import get_optional_user
from app.db.session import get_db
from app.models.course import Course
from app.models.enums import PublishStatus, UserRole
from app.models.lesson import Lesson
from app.models.module import Module
from app.schemas.course import CourseDetail, CourseOut, LessonOut, ModuleOut

router = APIRouter(tags=["courses"])


@router.get("/courses", response_model=list[CourseOut])
def list_courses(db: Session = Depends(get_db), user=Depends(get_optional_user)):
    q = select(Course)
    if not user or user.role != UserRole.ADMIN:
        q = q.where(Course.status == PublishStatus.PUBLISHED)
    return db.scalars(q.order_by(Course.id.desc())).all()


@router.get("/courses/{slug}", response_model=CourseDetail)
def get_course(slug: str, db: Session = Depends(get_db), user=Depends(get_optional_user)):
    course = db.scalar(select(Course).where(Course.slug == slug))
    if not course:
        raise HTTPException(404, "Course not found")
    if course.status != PublishStatus.PUBLISHED and (not user or user.role != UserRole.ADMIN):
        raise HTTPException(404, "Course not found")

    modules = db.scalars(select(Module).where(Module.course_id == course.id).order_by(Module.sort_order)).all()
    mod_out = []
    for m in modules:
        lessons = db.scalars(select(Lesson).where(Lesson.module_id == m.id).order_by(Lesson.sort_order)).all()
        mod_out.append(
            ModuleOut(
                id=m.id,
                course_id=m.course_id,
                title=m.title,
                description=m.description,
                sort_order=m.sort_order,
                lessons=[LessonOut.model_validate(l) for l in lessons],
            )
        )
    return CourseDetail(**CourseOut.model_validate(course).model_dump(), modules=mod_out)
