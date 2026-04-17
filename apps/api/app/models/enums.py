from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    LEARNER = "learner"


class PublishStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"


class LessonType(StrEnum):
    ARTICLE = "article"
    QUIZ = "quiz"
    EXERCISE = "exercise"
    SANDBOX = "sandbox"


class EnrollmentStatus(StrEnum):
    ACTIVE = "active"


class ProgressStatus(StrEnum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
