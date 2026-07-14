from pydantic import BaseModel

from .analysis import MatchAnalysis
from .cover_letter import CoverLetter
from .job import Job
from .match import MatchResult
from .resume import Resume
from .tailored_resume import TailoredResume

class PipelineResult(BaseModel):
    """Results produced by the end-to-end application pipeline."""

    resume: Resume
    job: Job
    match: MatchResult
    analysis: MatchAnalysis
    tailored_resume: TailoredResume
    cover_letter: CoverLetter