from pydantic import BaseModel

class MatchResult(BaseModel):
    matching_skills: list[str]
    missing_skills: list[str]
    extra_skills: list[str]
    match_percentage: float