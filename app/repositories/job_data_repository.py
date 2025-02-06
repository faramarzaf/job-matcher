from app.core.config import settings
from app.core.database import db
from app.models.job import Job


class JobDataRepository:
    @staticmethod
    async def store_jobs(jobs):
        collection = db.client[settings.DATABASE_NAME].jobs
        await collection.delete_many({})
        job_documents = [Job(**job).dict(by_alias=True) for job in jobs]
        if job_documents:
            await collection.insert_many(job_documents)

    @staticmethod
    async def get_all_jobs():
        collection = db.client[settings.DATABASE_NAME].jobs
        job_docs = await collection.find().to_list(length=100)
        return [Job(**job) for job in job_docs]  # ✅ Ensure proper Job objects

    @staticmethod
    async def get_jobs_matching_skills(skills):
        collection = db.client[settings.DATABASE_NAME].jobs
        query = {"skills": {"$in": skills}}
        job_docs = await collection.find(query).to_list(length=100)
        return [Job(**job) for job in job_docs]  # ✅ Ensure valid Job objects
