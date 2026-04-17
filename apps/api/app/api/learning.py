from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.lesson import Lesson
from app.models.module import Module
from app.models.quiz import Quiz, QuizAttempt, QuizQuestion
from app.models.sandbox import SandboxRun, SandboxTask
from app.schemas.course import CourseProgressOut
from app.schemas.quiz import QuizOut, QuizQuestionOut, QuizSubmitRequest, QuizSubmitResponse
from app.schemas.sandbox import SandboxRunOut, SandboxTaskOut
from app.services.progress_service import course_progress, set_lesson_completed, set_lesson_started
from app.services.quiz_service import submit_quiz
from app.services.sandbox_service import run_prompt_sandbox

router = APIRouter(tags=["learning"])


def ensure_enrolled(db: Session, user_id: int, lesson_id: int) -> None:
    course_id = db.scalar(
        select(Module.course_id).join(Lesson, Lesson.module_id == Module.id).where(Lesson.id == lesson_id)
    )
    if not course_id:
        raise HTTPException(404, "Lesson not found")
    enrollment = db.scalar(
        select(Enrollment).where(Enrollment.user_id == user_id, Enrollment.course_id == course_id)
    )
    if not enrollment:
        raise HTTPException(403, "You must enroll in this course first")


@router.post("/courses/{course_id}/enroll")
def enroll(course_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(404, "Course not found")
    existing = db.scalar(select(Enrollment).where(Enrollment.user_id == user.id, Enrollment.course_id == course_id))
    if existing:
        return {"message": "Already enrolled"}
    enr = Enrollment(user_id=user.id, course_id=course_id)
    db.add(enr)
    db.commit()
    return {"message": "Enrolled"}


@router.get("/me/enrollments")
def my_enrollments(user=Depends(get_current_user), db: Session = Depends(get_db)):
    enrollments = db.scalars(select(Enrollment).where(Enrollment.user_id == user.id)).all()
    payload = []
    for enrollment in enrollments:
        course = db.get(Course, enrollment.course_id)
        payload.append(
            {
                "id": enrollment.id,
                "course_id": enrollment.course_id,
                "course_slug": course.slug if course else None,
                "course_title": course.title if course else None,
                "enrolled_at": enrollment.enrolled_at,
                "status": enrollment.status,
            }
        )
    return payload


@router.post("/lessons/{lesson_id}/start")
def lesson_start(lesson_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    ensure_enrolled(db, user.id, lesson_id)
    return set_lesson_started(db, user.id, lesson_id)


@router.post("/lessons/{lesson_id}/complete")
def lesson_complete(lesson_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    ensure_enrolled(db, user.id, lesson_id)
    return set_lesson_completed(db, user.id, lesson_id)


@router.get("/me/courses/{course_id}/progress", response_model=CourseProgressOut)
def my_progress(course_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return course_progress(db, user.id, course_id)


@router.get("/lessons/{lesson_id}/quiz", response_model=QuizOut)
def lesson_quiz(lesson_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    ensure_enrolled(db, user.id, lesson_id)
    quiz = db.scalar(select(Quiz).where(Quiz.lesson_id == lesson_id))
    if not quiz:
        raise HTTPException(404, "Quiz not found")
    questions = db.scalars(
        select(QuizQuestion).where(QuizQuestion.quiz_id == quiz.id).order_by(QuizQuestion.sort_order)
    ).all()
    return QuizOut(
        id=quiz.id,
        lesson_id=quiz.lesson_id,
        title=quiz.title,
        passing_score=quiz.passing_score,
        questions=[
            QuizQuestionOut(
                id=q.id,
                question_text=q.question_text,
                options_json=q.options_json,
                explanation=q.explanation,
            )
            for q in questions
        ],
    )


@router.post("/quizzes/{quiz_id}/submit", response_model=QuizSubmitResponse)
def quiz_submit(quiz_id: int, payload: QuizSubmitRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    quiz = db.get(Quiz, quiz_id)
    if not quiz:
        raise HTTPException(404, "Quiz not found")
    ensure_enrolled(db, user.id, quiz.lesson_id)

    attempt = submit_quiz(db, user.id, quiz_id, [a.model_dump() for a in payload.answers])
    lesson = db.scalar(select(Lesson).where(Lesson.id == quiz.lesson_id))
    if lesson:
        set_lesson_completed(db, user.id, lesson.id)
    return QuizSubmitResponse(attempt_id=attempt.id, score=attempt.score, passed=attempt.passed)


@router.get("/me/quizzes/{quiz_id}/attempts")
def attempts(quiz_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.scalars(
        select(QuizAttempt).where(QuizAttempt.quiz_id == quiz_id, QuizAttempt.user_id == user.id)
    ).all()


@router.get("/lessons/{lesson_id}/sandbox", response_model=SandboxTaskOut)
def lesson_sandbox(lesson_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    ensure_enrolled(db, user.id, lesson_id)
    task = db.scalar(select(SandboxTask).where(SandboxTask.lesson_id == lesson_id))
    if not task:
        raise HTTPException(404, "Sandbox task not found")
    return task


@router.post("/sandbox/tasks/{task_id}/run", response_model=SandboxRunOut)
def sandbox_run(task_id: int, payload: dict, user=Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.get(SandboxTask, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    ensure_enrolled(db, user.id, task.lesson_id)
    run = run_prompt_sandbox(db, user.id, task, payload.get("submitted_content", ""))
    if run.score_or_result.get("passed"):
        lesson = db.scalar(select(Lesson).where(Lesson.id == task.lesson_id))
        if lesson:
            set_lesson_completed(db, user.id, lesson.id)
    return run


@router.get("/me/sandbox/runs")
def my_runs(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.scalars(
        select(SandboxRun).where(SandboxRun.user_id == user.id).order_by(SandboxRun.id.desc())
    ).all()
