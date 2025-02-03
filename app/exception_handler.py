from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status

# from pymongo.errors import CollectionInvalid

from .main import logger



class AppException(Exception):
    """This is the base class for all app errors"""
    pass


class InvalidId(AppException):
    """User has provided an invalid candidate id"""
    pass

class CustomBotoCoreError(AppException):
    """Custom error to handle BotoCore related Exceptions"""
    pass


class CustomClientError(AppException):
    """Custom error to handle Client related Exceptions"""
    pass


class BackgroundTaskError(AppException):
    """Custom error to handle Exceptions in background tasks"""
    pass

def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exc: AppException):
        logger.error(f"An error occurred: {exc} Request: {request}")
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler

def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        InvalidId,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "A context with this candidate_id does not exist.",
                "error_code": "invalid_candidate_id",
            },
        ),
    )

    app.add_exception_handler(
        CustomBotoCoreError,
        create_exception_handler(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            initial_detail={
                "message": "A BotoCore error occurred",
                "error_code": "boto_core_error",
            },
        ),
    )

    app.add_exception_handler(
        CustomClientError,
        create_exception_handler(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            initial_detail={
                "message": "A Client error occurred",
                "error_code": "client_error",
            },
        ),
    )

    app.add_exception_handler(
        BackgroundTaskError,
        create_exception_handler(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            initial_detail={
                "message": "A Background Task error occurred",
                "error_code": "background_task",
            },
        ),
    )