from datetime import datetime
from pydantic import BaseModel


class SandboxTaskOut(BaseModel):
    id: int
    lesson_id: int
    title: str
    instructions: str
    starter_template: str
    runtime_type: str


class SandboxRunRequest(BaseModel):
    submitted_content: str


class SandboxRunOut(BaseModel):
    id: int
    status: str
    output: str
    logs: str
    score_or_result: dict
    created_at: datetime
