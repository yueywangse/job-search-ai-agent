from models import Resume
from prompts import RESUME_ANALYSIS_PROMPT
from services import LLM


class ResumeExtractor:
    """Extract structured resume information using an LLM."""

    def __init__(self):
        """Initialize the resume extractor."""

        self.llm = LLM()

    def extract(self, resume_text: str) -> Resume:
        """Extract structured information from a resume."""

        prompt = RESUME_ANALYSIS_PROMPT.format(resume=resume_text)

        return self.llm.generate(prompt, schema=Resume)
