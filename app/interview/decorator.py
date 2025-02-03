from app.main import logger
from app.exception_handler import BackgroundTaskError


def handle_background_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"An error occurred in background task: {str(e)}")
            raise BackgroundTaskError(f"An error occurred in background task: {str(e)}") from e

    return wrapper
