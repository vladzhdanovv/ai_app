import uuid
from typing import Annotated

from pydantic import BaseModel, AfterValidator, UUID4
from app.interview.dependencies import ScoreInt


class InterviewContext(BaseModel):
    job_title: str
    candidate_id: str
    questions: tuple[str, str, str] | None = None
    responses: tuple[str, str, str] | None = None
    scores: tuple[ScoreInt, ScoreInt, ScoreInt] | None = None
    feedback: str | None = None


class InterviewFileLogEntry(BaseModel):
    questions: tuple[str, str, str]
    responses: tuple[str, str, str]
    scores: tuple[ScoreInt, ScoreInt, ScoreInt]
    feedback: str


class InterviewStartEvent(BaseModel):
    job_title: str


class InterviewStartEventReceived(BaseModel):
    job_title: str
    candidate_id: UUID4 | Annotated[str, AfterValidator(lambda x: uuid.UUID(x, version=4))]
    questions: tuple[str, str, str]


class InterviewSubmitEvent(BaseModel):
    responses: tuple[str, str, str]


class InterviewSubmitEventReceived(BaseModel):
    job_title: str
    questions: tuple[str, str, str]
    responses: tuple[str, str, str]
    scores: tuple[ScoreInt, ScoreInt, ScoreInt]
    feedback: str

class InterviewLogEntry(BaseModel):
    candidate_id: str
    job_title: str
    dt: str | None = None
    file_path: str | None = None