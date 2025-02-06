from app.core.database import db, settings
from app.models.user import User


class UserRepository:
    @staticmethod
    async def create_user(email: str) -> str:
        document = {"email": email}
        result = await db.client[settings.DATABASE_NAME].users.insert_one(document)
        return str(result.inserted_id)

    @staticmethod
    async def get_user_by_email(email: str) -> User:
        document = await db.client[settings.DATABASE_NAME].users.find_one({"email": email})
        return User(**document) if document else None
