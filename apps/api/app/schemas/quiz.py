from datetime import datetime
from pydantic import BaseModel


class QuizQuestionOut(BaseModel):
    id: int
    question_text: str
    options_json: list[str]
    explanation: str


class QuizOut(BaseModel):
    id: int
    lesson_id: int
    title: str
    passing_score: int
    questions: list[QuizQuestionOut]


class SubmitAnswer(BaseModel):
    question_id: int
    selected_indexes: list[int]


class QuizSubmitRequest(BaseModel):
    answers: list[SubmitAnswer]


class QuizSubmitResponse(BaseModel):
    attempt_id: int
    score: int
    passed: bool


class QuizAttemptOut(BaseModel):
    id: int
    score: int
    passed: bool
    submitted_at: datetime
