import json
import logging
import os
import re
import tempfile

import pdfplumber
import spacy
from fastapi import HTTPException, UploadFile

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class CVExtractionService:
    COMMON_SKILLS = {
        "programming": ["python", "java", "javascript", "c++", "ruby", "php", "golang", "rust", "cobol", "html"],
        "frameworks": ["django", "flask", "spring", "react", "angular", "vue", "node"],
        "databases": ["sql", "mongodb", "postgresql", "mysql", "redis", "elasticsearch", "oracle", "sqlserver"],
        "tools": ["git", "docker", "kubernetes", "jenkins", "jira", "keycloak", "aws", "azure", "gcp"],

        "sales": ["cold calling", "negotiation", "lead generation", "sales pitch", "crm", "sales forecasting",
                  "b2b sales", "account management", "customer retention"],

        "digital_media": ["seo", "social media management", "content creation", "video editing", "google analytics",
                          "brand awareness", "online advertising", "copywriting", "email marketing"],

        "business_development": ["storytelling", "project management", "research", "strategic planning",
                                 "customer acquisition",
                                 "partnership development", "competitive analysis", "financial modeling",
                                 "revenue forecasting"],
    }

    RELEVANT_INDUSTRIES = ['Information-Technology', 'Sales', 'Digital-Media', 'Business-Development']

    @staticmethod
    async def extract_cv_data(pdf_file: UploadFile):
        if not pdf_file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = os.path.join(temp_dir, "temp.pdf")
                content = await pdf_file.read()

                if not content:
                    raise ValueError("Empty file")

                with open(temp_path, "wb") as f:
                    f.write(content)

                extracted_text = CVExtractionService._extract_text_from_pdf(temp_path)
                if not extracted_text:
                    raise ValueError("No text could be extracted from the PDF")

                skills = CVExtractionService._extract_skills(extracted_text)

                with open("skills.json", "r") as f:
                    skills_mapping = json.load(f)

                # ✅ Validate if extracted skills belong to IT, Sales, or Product
                is_valid_cv = any(
                    skill.lower() in [s.lower() for s in skills_mapping[industry]]
                    for industry in CVExtractionService.RELEVANT_INDUSTRIES
                    for skill in skills
                )

                if not is_valid_cv:
                    raise HTTPException(status_code=400, detail="Only IT, Sales, and Product CVs are accepted.")

                return skills

        except HTTPException as he:
            raise he
        except Exception as e:
            logging.error(f"Error while extracting CV data: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def _extract_text_from_pdf(pdf_path: str) -> str:
        with pdfplumber.open(pdf_path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)

    @staticmethod
    def _extract_skills(text: str) -> list:
        text_lower = text.lower()
        skills = set()

        for category, skill_list in CVExtractionService.COMMON_SKILLS.items():
            for skill in skill_list:
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if re.search(pattern, text_lower):
                    skills.add(skill.title())

        return sorted(list(skills))
