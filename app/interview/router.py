from fastapi import APIRouter, BackgroundTasks

from .model import (InterviewContext, InterviewStartEvent, InterviewStartEventReceived, InterviewSubmitEvent,
                    InterviewSubmitEventReceived)

from app.dependencies import (CacheDep, ConfigDep, AwsSessionDep)
from app.exception_handler import InvalidId
from .dependencies import AssignCandidateIdDep
from .background_task import save_data

interview_router = APIRouter()

fake_q = ('one', 'two', 'three')
fake_s = (1, 2, 3)
fake_f = 'lorem ipsum'


@interview_router.post("/start",
                        summary="Start a new interview.",
                        response_model=InterviewStartEventReceived)
async def start_interview(
        request: InterviewStartEvent,
        candidate_id: AssignCandidateIdDep,
        cache: CacheDep,
):
    """Start a new interview."""
    context = InterviewContext(job_title=request.job_title, candidate_id=str(candidate_id))
    context.questions = fake_q
    await cache.set(candidate_id, context.model_dump())

    return context


@interview_router.post("/{candidate_id}/submit",
                        summary="Submit responses and receive feedback.",
                        response_model=InterviewSubmitEventReceived
                       )
async def submit_interview(
        candidate_id: str,
        request: InterviewSubmitEvent,
        cache: CacheDep,
        config: ConfigDep,
        aws_session: AwsSessionDep,
        background_tasks: BackgroundTasks
) -> InterviewSubmitEventReceived:
    """Submit responses and receive feedback."""

    cached_context = await cache.get(candidate_id)
    if not cached_context:
        raise InvalidId()

    context = InterviewContext(**cached_context)

    context.responses = request.responses
    context.scores = fake_s
    context.feedback = fake_f

    data = context.model_dump()
    await cache.set(candidate_id, data)

    # AWS bucket and table name
    bucket = 'ai-app-filestorage'
    table_name = 'ai_app'

    background_tasks.add_task(save_data, aws_session, data, bucket, table_name)

    return InterviewSubmitEventReceived(**data)
