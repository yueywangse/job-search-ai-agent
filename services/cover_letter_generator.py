from models import CoverLetter, Job, Resume, TailoredResume
from prompts import COVER_LETTER_PROMPT
from services import LLM


class CoverLetterGenerator:
    """Generate a tailored cover letter using an LLM."""

    def __init__(self, llm: LLM):
        """Initialize the cover letter generator."""

        self.llm = llm

    def generate(
        self, resume: Resume, tailored_resume: TailoredResume, job: Job, analysis: str, previous_cover_letter: CoverLetter | None, user_request: str
    ) -> CoverLetter:
        """Generate a cover letter tailored to the supplied job."""

        prompt = COVER_LETTER_PROMPT.format(
            resume=resume.model_dump_json(indent=2),
            tailored_resume=tailored_resume.model_dump_json(indent=2),
            job=job.model_dump_json(indent=2),
            analysis=analysis,
            previous_cover_letter=(
                previous_cover_letter.model_dump_json(indent=2)
                if previous_cover_letter
                else "None"
            ),
            user_request=user_request
        )

        return self.llm.generate(prompt, schema=CoverLetter)
