from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.quiz import Quiz, QuizAttempt, QuizAttemptAnswer, QuizQuestion


def submit_quiz(db: Session, user_id: int, quiz_id: int, answers: list[dict]):
    quiz = db.get(Quiz, quiz_id)
    questions = db.scalars(select(QuizQuestion).where(QuizQuestion.quiz_id == quiz_id)).all()
    q_map = {q.id: q for q in questions}
    correct = 0

    attempt = QuizAttempt(user_id=user_id, quiz_id=quiz_id, submitted_at=datetime.utcnow())
    db.add(attempt)
    db.flush()

    for answer in answers:
        q = q_map[answer["question_id"]]
        submitted = sorted(answer["selected_indexes"])
        expected = sorted(q.correct_answer_json)
        is_correct = submitted == expected
        if is_correct:
            correct += 1
        db.add(
            QuizAttemptAnswer(
                quiz_attempt_id=attempt.id,
                question_id=q.id,
                submitted_answer_json=submitted,
                is_correct=is_correct,
            )
        )

    score = int((correct / len(questions)) * 100) if questions else 0
    attempt.score = score
    attempt.passed = score >= quiz.passing_score
    db.commit()
    db.refresh(attempt)
    return attempt
