from typing import Annotated

from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends, Request

from .config import Settings, get_config
from .session import AwsSession
from .cache import RedisCache

async def get_mongo_client(request: Request):
    return request.app.state.mongo_client

def get_aws_session(request: Request) -> AwsSession:
    return request.app.state.aws_session


ConfigDep = Annotated[Settings, Depends(get_config)]
CacheDep = Annotated[RedisCache, Depends(RedisCache.get_cache)]
MongoDep = Annotated[AsyncIOMotorClient, Depends(get_mongo_client)]
AwsSessionDep = Annotated[AwsSession, Depends(get_aws_session)]

