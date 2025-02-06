from bson import ObjectId

from app.core.database import db, settings
from app.models.cv_data import CVData


class CVDataRepository:

    @staticmethod
    async def create_or_update_cv_data(user_id: str, skills: list) -> str:
        collection = db.client[settings.DATABASE_NAME].cv_data

        existing_cv = await collection.find_one({"user_id": ObjectId(user_id)})

        if existing_cv:
            # ✅ Update the existing CV record
            await collection.update_one(
                {"user_id": ObjectId(user_id)},
                {"$set": {"skills": skills}}
            )
            return str(existing_cv["_id"])  # Return the same CV ID

        else:
            # ✅ Create a new CV record if none exists
            document = {
                "user_id": ObjectId(user_id),
                "skills": skills
            }
            result = await collection.insert_one(document)
            return str(result.inserted_id)

    @staticmethod
    async def create_cv_data(user_id: str, skills: list) -> str:
        document = {
            "user_id": ObjectId(user_id),
            "skills": skills
        }
        result = await db.client[settings.DATABASE_NAME].cv_data.insert_one(document)
        return str(result.inserted_id)

    @staticmethod
    async def get_cv_data(user_id: str) -> CVData:
        document = await db.client[settings.DATABASE_NAME].cv_data.find_one({"user_id": ObjectId(user_id)})
        return CVData(**document) if document else None
