from models import InterviewAnswer
from prompts import INTERVIEW_ANSWER_PROMPT

from .llm import LLM

class InterviewAnswerGenerator:
    """Generate personalized interview answers."""

    def __init__(self, llm: LLM) -> None:
        self.llm = llm

    def generate(
        self,
        resume,
        tailored_resume,
        job,
        analysis,
        question: str,
    ) -> InterviewAnswer:
        prompt = INTERVIEW_ANSWER_PROMPT.format(
            resume=resume.model_dump_json(indent=2),
            tailored_resume=tailored_resume.model_dump_json(indent=2),
            job=job.model_dump_json(indent=2),
            analysis=analysis.model_dump_json(indent=2),
            question=question,
        )

        return self.llm.generate(
            prompt=prompt,
            schema=InterviewAnswer,
        )