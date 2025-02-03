from loguru import logger
from fastapi import FastAPI, Depends, status, Request, Response
from .api import api_router
from .exception_handler import register_all_errors
from .middleware import register_middleware
from .lifespan import lifespan

logger.add("logs/app.log", level="DEBUG")

class ApplicationBuilder:
    def __init__(self):
        self.app = FastAPI(title="AI APP", lifespan=lifespan)

    def build(self) -> FastAPI:
        self.app.include_router(api_router, prefix='/api/v1')
        register_all_errors(self.app)
        register_middleware(self.app)
        return self.app


builder = ApplicationBuilder()
app = builder.build()
