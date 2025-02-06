from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.user import PyObjectId


class CVData(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    skills: List[str] = []

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "user_id": "60dbf2b174d1d82f88c40c1a",
                "skills": ["Python", "Django", "React"]
            }
        }
    }
