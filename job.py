from pydantic import BaseModel

class Job(BaseModel):
    title: str
    company: str
    required_skills: list[str]
    preferred_skills: list[str]
    responsibilities: list[str]
    location: str