from fastapi import APIRouter, BackgroundTasks

from .model import (InterviewContext, InterviewStartEvent, InterviewStartEventReceived, InterviewSubmitEvent,
                    InterviewSubmitEventReceived)

from app.dependencies import (CacheDep, ConfigDep, AwsSessionDep)
from app.exception_handler import InvalidId
from app.agents.dependencies import WorkflowDep
from .dependencies import AssignCandidateIdDep
from .background_task import save_data

interview_router = APIRouter()

@interview_router.post("/start",
                        summary="Start a new interview.",
                        response_model=InterviewStartEventReceived)
async def start_interview(
        request: InterviewStartEvent,
        candidate_id: AssignCandidateIdDep,
        cache: CacheDep,
        workflow: WorkflowDep
) -> InterviewSubmitEventReceived:
    """Start a new interview."""
    context = InterviewContext(job_title=request.job_title, candidate_id=str(candidate_id))
    context = await workflow.run(context)
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
        background_tasks: BackgroundTasks,
        workflow: WorkflowDep
) -> InterviewSubmitEventReceived:
    """Submit responses and receive feedback."""

    cached_context = await cache.get(candidate_id)
    if not cached_context:
        raise InvalidId()

    context = InterviewContext(**cached_context)

    context.responses = request.responses
    context = await workflow.run(context)

    data = context.model_dump()
    await cache.set(candidate_id, data)

    background_tasks.add_task(save_data, aws_session, data, config.aws_bucket, config.aws_table)

    return InterviewSubmitEventReceived(**data)
