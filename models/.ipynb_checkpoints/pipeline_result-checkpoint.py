from pydantic import BaseModel

from .analysis import MatchAnalysis
from .cover_letter import CoverLetter
from .job import Job
from .match import MatchResult
from .resume import Resume
from .tailored_resume import TailoredResume
from .interview_questions import InterviewQuestions

class PipelineResult(BaseModel):
    """Results produced by the end-to-end application pipeline."""

    resume: Resume
    job: Job
    match: MatchResult
    analysis: MatchAnalysis
    tailored_resume: TailoredResume
    cover_letter: CoverLetter | None = None
    interview_questions: InterviewQuestions | None = None
    
    original_match: MatchResult | None = None
    tailored_match: MatchResult | None = None
    original_coverage: float | None = None
    tailored_coverage: float | None = None