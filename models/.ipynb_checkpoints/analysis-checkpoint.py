from pydantic import BaseModel

class MatchAnalysis(BaseModel):
    """Detailed analysis of the resume-job match."""

    summary: str
    strengths: list[str]
    gaps: list[str]
    resume_improvements: list[str]
    interview_risks: list[str]
