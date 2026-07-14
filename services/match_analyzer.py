from models import Job, MatchAnalysis, MatchResult, Resume
from prompts import MATCH_ANALYSIS_PROMPT
from services import LLM


class MatchAnalyzer:
    """Analyze how well a resume matches a job description."""

    def __init__(self):
        """Initialize the match analyzer."""

        self.llm = LLM()

    def analyze(self, resume: Resume, job: Job, match: MatchResult) -> MatchAnalysis:
        """Generate a detailed analysis of the resume-job match."""

        prompt = MATCH_ANALYSIS_PROMPT.format(
            resume=resume.model_dump_json(indent=2),
            job=job.model_dump_json(indent=2),
            match=match.model_dump_json(indent=2),
        )

        return self.llm.generate(prompt, schema=MatchAnalysis)
