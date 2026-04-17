from pydantic import BaseModel, Field
from app.models.enums import LessonType, PublishStatus, ProgressStatus


class LessonOut(BaseModel):
    id: int
    module_id: int
    title: str
    slug: str
    summary: str
    lesson_type: LessonType
    content_markdown: str
    estimated_minutes: int
    sort_order: int
    status: PublishStatus

    class Config:
        from_attributes = True


class ModuleOut(BaseModel):
    id: int
    course_id: int
    title: str
    description: str
    sort_order: int
    lessons: list[LessonOut] = Field(default_factory=list)


class CourseOut(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    difficulty: str
    estimated_minutes: int
    tags: list[str]
    thumbnail_url: str
    status: PublishStatus

    class Config:
        from_attributes = True


class CourseDetail(CourseOut):
    modules: list[ModuleOut]


class CourseCreate(BaseModel):
    title: str
    slug: str
    description: str = ""
    difficulty: str = "beginner"
    estimated_minutes: int = 60
    tags: list[str] = Field(default_factory=list)
    thumbnail_url: str = ""
    status: PublishStatus = PublishStatus.DRAFT


class ModuleCreate(BaseModel):
    title: str
    description: str = ""
    sort_order: int = 0


class LessonCreate(BaseModel):
    title: str
    slug: str
    summary: str = ""
    lesson_type: LessonType
    content_markdown: str = ""
    estimated_minutes: int = 10
    sort_order: int = 0
    status: PublishStatus = PublishStatus.DRAFT


class ProgressOut(BaseModel):
    lesson_id: int
    status: ProgressStatus


class CourseProgressOut(BaseModel):
    course_id: int
    completion_percent: float
    completed_lessons: int
    total_lessons: int
    last_lesson_slug: str | None = None
