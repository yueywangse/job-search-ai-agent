from pydantic import BaseModel
from .resume import Experience, Project

class TailoredResume(BaseModel):
    """Tailored resume content generated for a specific job."""

    professional_summary: str
    skills: list[str]
    work_experience: list[Experience]
    projects: list[Project]
