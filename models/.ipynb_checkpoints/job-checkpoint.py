from pydantic import BaseModel

class Job(BaseModel):
    """Structured representation of a job description."""

    title: str
    company: str
    required_skills: list[str]
    preferred_skills: list[str]
    responsibilities: list[str]
    location: str
