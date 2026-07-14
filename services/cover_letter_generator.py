from models import CoverLetter, Job, Resume, TailoredResume
from prompts import COVER_LETTER_PROMPT
from services import LLM


class CoverLetterGenerator:
    """Generate a tailored cover letter using an LLM."""

    def __init__(self):
        """Initialize the cover letter generator."""

        self.llm = LLM()

    def generate(
        self, resume: Resume, tailored_resume: TailoredResume, job: Job, analysis: str
    ) -> CoverLetter:
        """Generate a cover letter tailored to the supplied job."""

        prompt = COVER_LETTER_PROMPT.format(
            resume=resume.model_dump_json(indent=2),
            tailored_resume=tailored_resume.model_dump_json(indent=2),
            job=job.model_dump_json(indent=2),
            analysis=analysis,
        )

        return self.llm.generate(prompt, schema=CoverLetter)
