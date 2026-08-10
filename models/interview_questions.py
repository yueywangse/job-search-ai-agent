from pydantic import BaseModel, Field

class InterviewQuestions(BaseModel):
    technical: list[str] = Field(default_factory=list)
    behavioral: list[str] = Field(default_factory=list)
    role_specific: list[str] = Field(default_factory=list)