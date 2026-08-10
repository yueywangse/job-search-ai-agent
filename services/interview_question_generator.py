from models import (
    InterviewQuestions,
    Job,
    MatchAnalysis,
    Resume,
    TailoredResume
)
from prompts import INTERVIEW_QUESTIONS_PROMPT
from services import LLM

class InterviewQuestionGenerator:
    """Generate interview questions for a job application."""

    def __init__(self, llm: LLM):
        self.llm = llm

    def generate(
        self,
        resume: Resume,
        tailored_resume: TailoredResume,
        job: Job,
        analysis: MatchAnalysis
    ) -> InterviewQuestions:
        """Generate interview questions."""

        prompt = INTERVIEW_QUESTIONS_PROMPT.format(
            resume=resume.model_dump_json(indent=2),
            tailored_resume=tailored_resume.model_dump_json(indent=2),
            job=job.model_dump_json(indent=2),
            analysis=analysis.model_dump_json(indent=2)
        )

        return self.llm.generate(
            prompt,
            schema=InterviewQuestions
        )