import redis.asyncio as redis
from app.core.config import settings

class RedisClient:
    def __init__(self):
        self._pool = None

    def init_pool(self):
        if not self._pool:
            if settings.REDIS_URL.startswith("mock://"):
                # Fake redis could be used here, but we will just leave it empty for now
                pass
            else:
                self._pool = redis.ConnectionPool.from_url(
                    settings.REDIS_URL,
                    decode_responses=True
                )

    async def get_connection(self):
        if not self._pool:
            self.init_pool()
        if settings.REDIS_URL.startswith("mock://"):
            return None # Handle mock if needed
        return redis.Redis(connection_pool=self._pool)

redis_client = RedisClient()
