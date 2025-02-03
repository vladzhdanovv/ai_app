import logging

from contextlib import asynccontextmanager

from motor.motor_asyncio import AsyncIOMotorClient

from fastapi import FastAPI
from .config import get_config, Settings
from .session import AwsSession


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # read configuration
        config: Settings = get_config()
        # establish MongoDB connection
        mongo_client = AsyncIOMotorClient(config.mongo_uri)
        # initiate AWS Session
        aws_session = AwsSession(config.aws_access_key_id, config.aws_secret_access_key, config.aws_region)


        # Check if the state attribute exists
        if not hasattr(app, 'state'):
            app.state = {}

        app.state.mongo_client = mongo_client
        app.state.aws_session = aws_session

        yield
    except Exception as e:
        logging.error(f'Exception occurred while establishing connections: {e}')
        raise
    finally:
        # clean up
        if hasattr(app.state, 'mongo_client'):
            app.state.mongo_client.close()
        if hasattr(app.state, 'aws_session'):
            del app.state.aws_session



