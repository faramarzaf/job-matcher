from typing import Optional, List, Any

from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic_core import core_schema


class PyObjectId(ObjectId):

    @classmethod
    def __get_pydantic_core_schema__(
            cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.union_schema([
                    core_schema.str_schema(),
                    core_schema.bytes_schema(),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )


class Job(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: str
    company: Optional[str] = None
    link: str
    description: str
    image: Optional[str] = None
    skills: List[str] = []
    pubDate: Optional[str] = None
    expires_at: Optional[str] = None
    guid: Optional[str] = None
    region: Optional[str] = None
    category: Optional[str] = None
    type: Optional[str] = None

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "title": "Software Engineer",
                "link": "https://example.com/job/software-engineer",
                "description": "Looking for a Python developer...",
                "image": "https://example.com/company-logo.png",
                "skills": ["Python", "Django", "REST APIs"],
                "pubDate": "2025-01-30T18:38:55Z",
                "expires_at": "2025-03-01T18:38:55Z",
                "guid": "https://example.com/job/123",
                "region": "Remote",
                "category": "Engineering",
                "type": "Full-Time",
            }
        }
    }
