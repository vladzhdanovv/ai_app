from typing import Annotated

from fastapi import Depends

from aiocache import Cache
from aiocache.serializers import JsonSerializer

from .config import Settings, get_config


class RedisCache:
    def __init__(self, config: Annotated[Settings, Depends(get_config)]):
        self.config = config

    def redis_cache_config(self) -> dict:
        return {
            'endpoint': self.config.redis_endpoint,
            'port': self.config.redis_port,
            'serializer': JsonSerializer()
        }

    @classmethod
    async def get_cache(cls, config: Annotated[Settings, Depends(get_config)]) -> Cache:
        instance = cls(config)
        cache_config = instance.redis_cache_config()
        return Cache(Cache.REDIS, **cache_config)
