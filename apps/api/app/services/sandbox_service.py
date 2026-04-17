from datetime import datetime
from sqlalchemy.orm import Session
from app.models.sandbox import SandboxRun, SandboxTask


def run_prompt_sandbox(db: Session, user_id: int, task: SandboxTask, submitted_content: str) -> SandboxRun:
    required_phrase = str(task.validator_config.get("must_include", "")).lower()
    is_pass = required_phrase in submitted_content.lower() if required_phrase else len(submitted_content.strip()) > 0
    output = "Validation passed" if is_pass else f"Response must include: {required_phrase}"
    run = SandboxRun(
        user_id=user_id,
        sandbox_task_id=task.id,
        submitted_content=submitted_content,
        output=output,
        logs="prompt sandbox evaluator",
        status="completed",
        score_or_result={"passed": is_pass},
        created_at=datetime.utcnow(),
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run
