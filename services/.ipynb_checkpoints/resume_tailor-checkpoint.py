from models import Job, Resume, TailoredResume
from prompts import RESUME_TAILOR_PROMPT
from services import LLM


class ResumeTailor:
    """Tailor a resume for a specific job using an LLM."""

    def __init__(self, llm: LLM):
        """Initialize the resume tailor."""

        self.llm = llm

    def tailor(self, resume: Resume, job: Job, analysis: str) -> TailoredResume:
        """Generate a tailored resume for the supplied job."""

        prompt = RESUME_TAILOR_PROMPT.format(
            resume=resume.model_dump_json(indent=2),
            job=job.model_dump_json(indent=2),
            analysis=analysis,
        )

        return self.llm.generate(prompt, schema=TailoredResume)
