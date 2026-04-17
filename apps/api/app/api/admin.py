from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.api.deps import require_admin
from app.db.session import get_db
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.enums import ProgressStatus
from app.models.lesson import Lesson
from app.models.module import Module
from app.models.progress import LessonProgress
from app.models.quiz import Quiz, QuizAttempt, QuizQuestion
from app.models.sandbox import SandboxTask
from app.models.user import User
from app.schemas.course import CourseCreate, CourseOut, LessonCreate, ModuleCreate
from app.schemas.sandbox import SandboxTaskOut

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])


@router.post("/courses", response_model=CourseOut)
def create_course(payload: CourseCreate, db: Session = Depends(get_db), user=Depends(require_admin)):
    if db.scalar(select(Course).where(Course.slug == payload.slug)):
        raise HTTPException(400, "Course slug already exists")
    course = Course(**payload.model_dump(), created_by=user.id)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.patch("/courses/{course_id}", response_model=CourseOut)
def update_course(course_id: int, payload: CourseCreate, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(404, "Course not found")
    slug_owner = db.scalar(select(Course).where(Course.slug == payload.slug, Course.id != course_id))
    if slug_owner:
        raise HTTPException(400, "Course slug already exists")
    for k, v in payload.model_dump().items():
        setattr(course, k, v)
    db.commit()
    db.refresh(course)
    return course


@router.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(404, "Course not found")
    db.delete(course)
    db.commit()
    return {"message": "deleted"}


@router.post("/courses/{course_id}/modules")
def create_module(course_id: int, payload: ModuleCreate, db: Session = Depends(get_db)):
    if not db.get(Course, course_id):
        raise HTTPException(404, "Course not found")
    module = Module(course_id=course_id, **payload.model_dump())
    db.add(module)
    db.commit()
    db.refresh(module)
    return module


@router.patch("/modules/{module_id}")
def update_module(module_id: int, payload: ModuleCreate, db: Session = Depends(get_db)):
    module = db.get(Module, module_id)
    if not module:
        raise HTTPException(404, "Module not found")
    for k, v in payload.model_dump().items():
        setattr(module, k, v)
    db.commit()
    return module


@router.post("/modules/{module_id}/lessons")
def create_lesson(module_id: int, payload: LessonCreate, db: Session = Depends(get_db)):
    if not db.get(Module, module_id):
        raise HTTPException(404, "Module not found")
    if db.scalar(select(Lesson).where(Lesson.slug == payload.slug)):
        raise HTTPException(400, "Lesson slug already exists")
    lesson = Lesson(module_id=module_id, **payload.model_dump())
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


@router.patch("/lessons/{lesson_id}")
def update_lesson(lesson_id: int, payload: LessonCreate, db: Session = Depends(get_db)):
    lesson = db.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    slug_owner = db.scalar(select(Lesson).where(Lesson.slug == payload.slug, Lesson.id != lesson_id))
    if slug_owner:
        raise HTTPException(400, "Lesson slug already exists")
    for k, v in payload.model_dump().items():
        setattr(lesson, k, v)
    db.commit()
    return lesson


@router.delete("/lessons/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    db.delete(lesson)
    db.commit()
    return {"message": "deleted"}


@router.post("/lessons/{lesson_id}/quiz")
def create_quiz(lesson_id: int, payload: dict, db: Session = Depends(get_db)):
    lesson = db.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    quiz = Quiz(lesson_id=lesson_id, title=payload.get("title", "Quiz"), passing_score=payload.get("passing_score", 70))
    db.add(quiz)
    db.flush()
    for idx, q in enumerate(payload.get("questions", [])):
        db.add(
            QuizQuestion(
                quiz_id=quiz.id,
                question_text=q["question_text"],
                options_json=q.get("options_json", []),
                correct_answer_json=q.get("correct_answer_json", []),
                explanation=q.get("explanation", ""),
                sort_order=idx,
            )
        )
    db.commit()
    return {"quiz_id": quiz.id}


@router.post("/lessons/{lesson_id}/sandbox", response_model=SandboxTaskOut)
def create_sandbox(lesson_id: int, payload: dict, db: Session = Depends(get_db)):
    if not db.get(Lesson, lesson_id):
        raise HTTPException(404, "Lesson not found")
    task = SandboxTask(
        lesson_id=lesson_id,
        title=payload["title"],
        instructions=payload.get("instructions", ""),
        starter_template=payload.get("starter_template", ""),
        validator_config=payload.get("validator_config", {}),
        runtime_type="prompt",
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/analytics/overview")
def overview(db: Session = Depends(get_db)):
    return {
        "total_courses": db.scalar(select(func.count(Course.id))) or 0,
        "total_learners": db.scalar(select(func.count(User.id))) or 0,
        "enrollments_count": db.scalar(select(func.count(Enrollment.id))) or 0,
        "lesson_completion_count": db.scalar(
            select(func.count(LessonProgress.id)).where(LessonProgress.status == ProgressStatus.COMPLETED)
        )
        or 0,
        "quiz_attempt_count": db.scalar(select(func.count(QuizAttempt.id))) or 0,
    }
