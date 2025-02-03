from fastapi import APIRouter, status

from app.interview.router import interview_router


api_router = APIRouter()

api_router.include_router(interview_router, prefix="/interviews", tags=["interviews"])
