import json
import logging

import feedparser
import spacy
from bs4 import BeautifulSoup

from app.models.job import Job
from app.repositories.job_data_repository import JobDataRepository

nlp = spacy.load("en_core_web_lg")

ALLOWED_CATEGORIES = {"Information-Technology", "Sales", "Business-Development", "Product"}

with open("skills.json", "r") as f:
    skills_mapping = json.load(f)

all_possible_skills = set(skill.lower() for skills in skills_mapping.values() for skill in skills)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class JobFetchService:
    @staticmethod
    async def fetch_and_store_jobs():
        logging.info("Fetching job data from RSS feed...")

        try:
            feed_url = "https://weworkremotely.com/remote-jobs.rss"
            feed = feedparser.parse(feed_url)

            jobs = []
            for entry in feed.entries:
                job_image = None
                if "media_content" in entry:
                    job_image = entry.media_content[0]['url'] if entry.media_content else None

                company_name = JobFetchService.extract_company_name(entry.title)
                clean_title = JobFetchService.clean_job_title(entry.title)

                logging.info(f"Processing job: {clean_title} | Company: {company_name}")

                skills = JobFetchService.extract_skills(entry.title, entry.summary)
                category = JobFetchService.infer_category(clean_title, skills)

                if category not in ALLOWED_CATEGORIES:
                    logging.info(f"Skipping job {clean_title} due to category mismatch.")
                    continue

                job = Job(
                    title=clean_title,
                    company=company_name,
                    link=entry.link,
                    description=entry.summary,
                    image=job_image,
                    skills=skills,
                    pubDate=entry.published if hasattr(entry, "published") else None,
                    expires_at=entry.expires if hasattr(entry, "expires") else None,
                    guid=entry.guid if hasattr(entry, "guid") else entry.link,
                    region=entry.region if hasattr(entry, "region") else "Worldwide",
                    category=category,
                    type=entry.type if hasattr(entry, "type") else "Unknown",
                )
                jobs.append(job.dict(by_alias=True))

            await JobDataRepository.store_jobs(jobs)
            logging.info(f"Successfully stored {len(jobs)} jobs.")

        except Exception as e:
            logging.error(f"Error while fetching jobs: {str(e)}")

    @staticmethod
    def extract_company_name(title: str) -> str:
        if ":" in title:
            return title.split(":")[0].strip()
        return "Unknown"

    @staticmethod
    def clean_job_title(title: str) -> str:
        if ":" in title:
            return title.split(":")[1].strip()
        return title

    @staticmethod
    def extract_skills(job_title: str, job_description: str) -> list:
        clean_text = BeautifulSoup(job_description, "html.parser").get_text().lower()
        extracted_skills = set()

        for category, skill_list in skills_mapping.items():
            for skill in skill_list:
                if skill.lower() in clean_text or skill.lower() in job_title.lower():
                    extracted_skills.add(skill)

        return sorted(extracted_skills)

    @staticmethod
    def infer_category(job_title: str, skills: list) -> str:
        title_lower = job_title.lower()

        for category, skill_list in skills_mapping.items():
            if any(skill.lower() in skills for skill in skill_list):
                return category

        if "product" in title_lower or "manager" in title_lower:
            return "Product"
        if any(term in title_lower for term in ["sales", "business development", "b2b"]):
            return "Sales"
        if any(term in title_lower for term in ["software", "developer", "engineer", "cloud", "ai", "cybersecurity"]):
            return "Information-Technology"

        return "Unknown"
