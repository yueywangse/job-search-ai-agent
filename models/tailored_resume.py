from pydantic import BaseModel, Field
from .resume import Experience, Project
from typing import Literal

class ResumeChangeReason(BaseModel):
    section: Literal["work_experience", "project"]
    item: str
    reason: str

class TailoredResume(BaseModel):
    """Tailored resume content generated for a specific job."""

    professional_summary: str
    skills: list[str]
    work_experience: list[Experience]
    projects: list[Project]
    change_reasons: list[ResumeChangeReason] = Field(default_factory=list)