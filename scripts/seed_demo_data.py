"""Seed realistic demo content for Learning Platform MVP."""

from sqlalchemy import select
from app.auth.security import hash_password
from app.db.session import SessionLocal
from app.models.course import Course
from app.models.enums import LessonType, PublishStatus, UserRole
from app.models.lesson import Lesson
from app.models.module import Module
from app.models.quiz import Quiz, QuizQuestion
from app.models.sandbox import SandboxTask
from app.models.user import User

CATALOG = [
    {
        "title": "Prompt Engineering Foundations",
        "slug": "prompt-engineering-foundations",
        "difficulty": "beginner",
        "modules": [
            {
                "title": "Prompt Basics",
                "lessons": [
                    ("article", "Instruction anatomy", "Understand role, task, constraints, and output formatting."),
                    ("quiz", "Prompt quality check", "Short MCQ quiz on specificity and grounding."),
                    ("sandbox", "Rewrite weak prompts", "Improve a vague prompt using a required rubric phrase."),
                ],
            },
            {
                "title": "Evaluation Patterns",
                "lessons": [
                    ("article", "Acceptance criteria", "Define pass/fail criteria for generated outputs."),
                    ("exercise", "Critique prompts", "Free-text reflection exercise for prompt critiques."),
                    ("sandbox", "Prompt stress test", "Submit a robust prompt that includes success metrics."),
                ],
            },
        ],
    },
    {
        "title": "Agentic AI Basics",
        "slug": "agentic-ai-basics",
        "difficulty": "beginner",
        "modules": [
            {
                "title": "Agent Loops",
                "lessons": [
                    ("article", "Plan-act-observe", "Lifecycle of a simple agent loop."),
                    ("quiz", "Loop comprehension", "MCQ on tool use and control flow."),
                    ("sandbox", "Draft an agent prompt", "Compose an agent prompt with a stopping rule."),
                ],
            },
            {
                "title": "Tooling & Guardrails",
                "lessons": [
                    ("article", "Tool schemas", "How to define deterministic tool signatures."),
                    ("exercise", "Guardrail checklist", "Write a minimal runtime guardrail checklist."),
                ],
            },
        ],
    },
    {
        "title": "RAG Essentials",
        "slug": "rag-essentials",
        "difficulty": "intermediate",
        "modules": [
            {
                "title": "Index & Retrieve",
                "lessons": [
                    ("article", "Chunking strategy", "Compare fixed-size and semantic chunking."),
                    ("quiz", "Retrieval pitfalls", "MCQ on recall vs precision tradeoffs."),
                ],
            },
            {
                "title": "Answer Synthesis",
                "lessons": [
                    ("article", "Grounded answering", "Citations-first response structure."),
                    ("sandbox", "Grounded response prompt", "Produce a prompt including citation requirements."),
                ],
            },
        ],
    },
    {
        "title": "Healthcare AI Workflow Design",
        "slug": "healthcare-ai-workflow-design",
        "difficulty": "intermediate",
        "modules": [
            {
                "title": "Clinical Documentation",
                "lessons": [
                    ("article", "SOAP summarization", "Convert notes into structured SOAP format."),
                    ("quiz", "Safety checks", "MCQ on hallucination and human review triggers."),
                ],
            },
            {
                "title": "Operations & Compliance",
                "lessons": [
                    ("article", "Auditability", "Capturing trace metadata for regulated workflows."),
                    ("sandbox", "Escalation protocol prompt", "Create a prompt that explicitly includes escalation criteria."),
                ],
            },
        ],
    },
]


def ensure_users(db):
    admin = db.scalar(select(User).where(User.email == "admin@demo.local"))
    if not admin:
        admin = User(
            email="admin@demo.local",
            full_name="Demo Admin",
            password_hash=hash_password("password123"),
            role=UserRole.ADMIN,
        )
        db.add(admin)
        db.flush()

    learner = db.scalar(select(User).where(User.email == "learner@demo.local"))
    if not learner:
        db.add(
            User(
                email="learner@demo.local",
                full_name="Demo Learner",
                password_hash=hash_password("password123"),
                role=UserRole.LEARNER,
            )
        )
    return admin


def seed():
    db = SessionLocal()
    admin = ensure_users(db)

    for course_data in CATALOG:
        if db.scalar(select(Course).where(Course.slug == course_data["slug"])):
            continue

        course = Course(
            title=course_data["title"],
            slug=course_data["slug"],
            description=f"Production-style MVP course: {course_data['title']}.",
            difficulty=course_data["difficulty"],
            estimated_minutes=180,
            tags=["ai", "learning", "mvp"],
            thumbnail_url="",
            status=PublishStatus.PUBLISHED,
            created_by=admin.id,
        )
        db.add(course)
        db.flush()

        lesson_counter = 1
        for module_index, module_data in enumerate(course_data["modules"], start=1):
            module = Module(
                course_id=course.id,
                title=module_data["title"],
                description=f"{module_data['title']} module content.",
                sort_order=module_index,
            )
            db.add(module)
            db.flush()

            for lesson_index, (lesson_type, lesson_title, lesson_summary) in enumerate(module_data["lessons"], start=1):
                slug = f"{course.slug}-m{module_index}-l{lesson_index}"
                lesson = Lesson(
                    module_id=module.id,
                    title=lesson_title,
                    slug=slug,
                    summary=lesson_summary,
                    lesson_type=LessonType(lesson_type),
                    content_markdown=f"## {lesson_title}\n\n{lesson_summary}\n\n- Key takeaway {lesson_counter}\n- Practical next step",
                    estimated_minutes=12,
                    sort_order=lesson_index,
                    status=PublishStatus.PUBLISHED,
                )
                db.add(lesson)
                db.flush()

                if lesson_type == "quiz":
                    quiz = Quiz(lesson_id=lesson.id, title=f"{lesson_title} Quiz", passing_score=70)
                    db.add(quiz)
                    db.flush()
                    db.add(
                        QuizQuestion(
                            quiz_id=quiz.id,
                            question_text="Which option best represents the safer and clearer approach?",
                            options_json=["Ambiguous instruction", "Explicit constraints and success criteria"],
                            correct_answer_json=[1],
                            explanation="Explicit requirements improve reliability and reviewability.",
                            sort_order=1,
                        )
                    )

                if lesson_type == "sandbox":
                    db.add(
                        SandboxTask(
                            lesson_id=lesson.id,
                            title=f"{lesson_title} Sandbox",
                            instructions="Submit a concise response that includes the phrase 'success criteria'.",
                            starter_template="You are an assistant helping a learner complete the task.",
                            validator_config={"must_include": "success criteria"},
                            runtime_type="prompt",
                        )
                    )

                lesson_counter += 1

    db.commit()
    db.close()


if __name__ == "__main__":
    seed()
    print("Demo data seeded")
