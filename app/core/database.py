from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


class Database:
    client: AsyncIOMotorClient = None

    @classmethod
    async def connect(cls):
        cls.client = AsyncIOMotorClient(settings.mongodb_uri)

    @classmethod
    async def disconnect(cls):
        if cls.client:
            cls.client.close()


db = Database()
