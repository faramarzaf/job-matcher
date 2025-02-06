import logging

from app.repositories.cv_data_repository import CVDataRepository
from app.repositories.job_data_repository import JobDataRepository

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class JobMatchingService:
    ALLOWED_CATEGORIES = {"Information-Technology", "Sales", "Business-Development", "Product"}

    @staticmethod
    async def recommend_jobs(user_id):
        logging.info(f"Fetching job recommendations for user: {user_id}")

        try:
            cv_data = await CVDataRepository.get_cv_data(user_id)
            if not cv_data or not cv_data.skills:
                logging.warning(f"No skills found for user {user_id}. Returning no recommendations.")
                return []
            user_skills = set(cv_data.skills)
            all_jobs = await JobDataRepository.get_all_jobs()
            filtered_jobs = [
                job for job in all_jobs if job.category in JobMatchingService.ALLOWED_CATEGORIES
            ]
            ranked_jobs = sorted(
                filtered_jobs,
                key=lambda job: (len(user_skills & set(job.skills)) * 2) +
                                (1 if job.category in JobMatchingService.ALLOWED_CATEGORIES else 0),
                reverse=True
            )
            return ranked_jobs[:10]

        except Exception as e:
            logging.error(f"Job matching failed for user {user_id}: {str(e)}")
            return []
