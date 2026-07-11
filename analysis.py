from pydantic import BaseModel

class MatchAnalysis(BaseModel):
    summary: str
    strengths: list[str]
    gaps: list[str]
    resume_improvements: list[str]
    interview_risks: list[str]